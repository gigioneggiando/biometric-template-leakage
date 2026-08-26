"""Optional InsightFace-backed ArcFace extraction with explicit model provenance."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Sequence
import numpy as np


_ARCFACE_DESTINATION = np.asarray(
    [[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366], [41.5493, 92.3655], [70.7299, 92.2041]],
    dtype=np.float32,
)


def _similarity_transform(source: np.ndarray, destination: np.ndarray) -> np.ndarray:
    source_mean = source.mean(axis=0)
    destination_mean = destination.mean(axis=0)
    source_centered = source - source_mean
    destination_centered = destination - destination_mean
    covariance = destination_centered.T @ source_centered / len(source)
    left, singular_values, right = np.linalg.svd(covariance)
    signs = np.ones(2, dtype=np.float64)
    if np.linalg.det(left) * np.linalg.det(right) < 0:
        signs[-1] = -1
    rotation = left @ np.diag(signs) @ right
    source_variance = np.mean(np.sum(source_centered ** 2, axis=1))
    scale = float(np.sum(singular_values * signs) / source_variance)
    linear = scale * rotation
    translation = destination_mean - linear @ source_mean
    return np.column_stack([linear, translation]).astype(np.float32)


def _nms(boxes: np.ndarray, scores: np.ndarray, threshold: float) -> np.ndarray:
    x1, y1, x2, y2 = boxes.T
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep: list[int] = []
    while order.size:
        index = int(order[0])
        keep.append(index)
        intersection_width = np.maximum(0.0, np.minimum(x2[index], x2[order[1:]]) - np.maximum(x1[index], x1[order[1:]]) + 1)
        intersection_height = np.maximum(0.0, np.minimum(y2[index], y2[order[1:]]) - np.maximum(y1[index], y1[order[1:]]) + 1)
        intersection = intersection_width * intersection_height
        overlap = intersection / (areas[index] + areas[order[1:]] - intersection)
        order = order[np.flatnonzero(overlap <= threshold) + 1]
    return np.asarray(keep, dtype=np.int64)


class ArcFaceExtractor:
    """Reusable InsightFace extractor for deterministic batch processing."""

    def __init__(
        self,
        model_root: str | Path,
        model_name: str = "antelopev2",
        providers: Sequence[str] = ("CUDAExecutionProvider", "CPUExecutionProvider"),
        detection_size: tuple[int, int] = (640, 640),
    ) -> None:
        try:
            from insightface.app import FaceAnalysis
        except ImportError as error:
            raise RuntimeError("Install optional face dependencies: python -m pip install -e '.[face]'") from error
        self._app: Any = FaceAnalysis(name=model_name, root=str(model_root), providers=list(providers))
        self._app.prepare(ctx_id=0, det_size=detection_size)

    def extract(self, image_path: str | Path) -> np.ndarray:
        """Extract and L2-normalize the largest detected face embedding."""
        from PIL import Image

        image = np.asarray(Image.open(image_path).convert("RGB"))[:, :, ::-1]
        faces = self._app.get(image)
        if not faces:
            raise ValueError(f"No face detected in {image_path}")
        face = max(faces, key=lambda value: (value.bbox[2] - value.bbox[0]) * (value.bbox[3] - value.bbox[1]))
        embedding = np.asarray(face.embedding, dtype=np.float32)
        if not np.all(np.isfinite(embedding)):
            raise ValueError("Non-finite ArcFace embedding")
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Zero-norm ArcFace embedding")
        return embedding / norm


class OpenCvArcFaceExtractor:
    """SCRFD alignment plus ArcFace inference through OpenCV's ONNX backend."""

    def __init__(
        self,
        recognition_model: str | Path,
        detection_model: str | Path,
        detection_size: tuple[int, int] = (640, 640),
        detection_threshold: float = 0.5,
    ) -> None:
        try:
            import cv2
        except ImportError as error:
            raise RuntimeError("Install optional face dependencies: python -m pip install -e '.[face]'") from error
        self._cv2: Any = cv2
        self._recognizer: Any = cv2.dnn.readNetFromONNX(str(recognition_model))
        self._detector: Any = cv2.dnn.readNetFromONNX(str(detection_model))
        self._detection_size = detection_size
        self._detection_threshold = detection_threshold

    def _detect_largest(self, image: np.ndarray) -> np.ndarray:
        cv2 = self._cv2
        target_width, target_height = self._detection_size
        scale = min(target_width / image.shape[1], target_height / image.shape[0])
        resized = cv2.resize(image, (round(image.shape[1] * scale), round(image.shape[0] * scale)))
        detector_input = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        detector_input[: resized.shape[0], : resized.shape[1]] = resized
        blob = cv2.dnn.blobFromImage(
            detector_input,
            1.0 / 128.0,
            self._detection_size,
            (127.5, 127.5, 127.5),
            swapRB=True,
        )
        self._detector.setInput(blob)
        outputs = self._detector.forward(self._detector.getUnconnectedOutLayersNames())
        if len(outputs) != 9:
            raise ValueError(f"Expected 9 SCRFD outputs, got {len(outputs)}")

        boxes_by_scale, scores_by_scale, landmarks_by_scale = [], [], []
        for output_index, stride in enumerate((8, 16, 32)):
            scores = np.asarray(outputs[output_index]).reshape(-1)
            box_distances = np.asarray(outputs[output_index + 3]) * stride
            landmark_distances = np.asarray(outputs[output_index + 6]) * stride
            grid_height, grid_width = target_height // stride, target_width // stride
            centers = np.stack(np.mgrid[:grid_height, :grid_width][::-1], axis=-1).astype(np.float32)
            centers = (centers * stride).reshape(-1, 2)
            anchors = len(scores) // len(centers)
            centers = np.repeat(centers, anchors, axis=0)
            positive = np.flatnonzero(scores >= self._detection_threshold)
            if not len(positive):
                continue
            boxes = np.column_stack(
                [
                    centers[:, 0] - box_distances[:, 0],
                    centers[:, 1] - box_distances[:, 1],
                    centers[:, 0] + box_distances[:, 2],
                    centers[:, 1] + box_distances[:, 3],
                ]
            )
            landmark_offsets = landmark_distances.reshape(-1, 5, 2)
            landmarks = centers[:, None, :] + landmark_offsets
            boxes_by_scale.append(boxes[positive] / scale)
            scores_by_scale.append(scores[positive])
            landmarks_by_scale.append(landmarks[positive] / scale)
        if not boxes_by_scale:
            raise ValueError("No face detected")

        boxes = np.vstack(boxes_by_scale)
        scores = np.concatenate(scores_by_scale)
        landmarks = np.vstack(landmarks_by_scale)
        kept = _nms(boxes, scores, 0.4)
        kept_boxes = boxes[kept]
        areas = (kept_boxes[:, 2] - kept_boxes[:, 0]) * (kept_boxes[:, 3] - kept_boxes[:, 1])
        return landmarks[kept[int(np.argmax(areas))]]

    def extract(self, image_path: str | Path) -> np.ndarray:
        """Detect, align, and extract one L2-normalized 512-D embedding."""
        cv2 = self._cv2
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Unable to read image {image_path}")
        landmarks = self._detect_largest(image)
        transform = _similarity_transform(landmarks, _ARCFACE_DESTINATION)
        aligned = cv2.warpAffine(image, transform, (112, 112), borderValue=0.0)
        blob = cv2.dnn.blobFromImage(
            aligned,
            1.0 / 127.5,
            (112, 112),
            (127.5, 127.5, 127.5),
            swapRB=True,
        )
        self._recognizer.setInput(blob)
        embedding = np.asarray(self._recognizer.forward(), dtype=np.float32).reshape(-1)
        if not np.all(np.isfinite(embedding)):
            raise ValueError("Non-finite ArcFace embedding")
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Zero-norm ArcFace embedding")
        return embedding / norm


class OpenCvYuNetArcFaceExtractor:
    """YuNet five-point alignment plus ArcFace inference through OpenCV."""

    def __init__(
        self,
        recognition_model: str | Path,
        detection_model: str | Path,
        detection_threshold: float = 0.5,
    ) -> None:
        try:
            import cv2
        except ImportError as error:
            raise RuntimeError("Install optional face dependencies: python -m pip install -e '.[face]'") from error
        self._cv2: Any = cv2
        self._recognizer: Any = cv2.dnn.readNetFromONNX(str(recognition_model))
        self._detector: Any = cv2.FaceDetectorYN.create(
            str(detection_model),
            "",
            (320, 320),
            detection_threshold,
            0.3,
            5000,
        )

    def _detect_largest(self, image: np.ndarray) -> np.ndarray:
        self._detector.setInputSize((image.shape[1], image.shape[0]))
        _, detections = self._detector.detect(image)
        if detections is None or not len(detections):
            raise ValueError("No face detected")
        face = max(detections, key=lambda row: row[2] * row[3])
        return np.asarray(face[4:14], dtype=np.float32).reshape(5, 2)

    def extract(self, image_path: str | Path) -> np.ndarray:
        """Detect, align, and extract one L2-normalized 512-D embedding."""
        cv2 = self._cv2
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Unable to read image {image_path}")
        landmarks = self._detect_largest(image)
        transform = _similarity_transform(landmarks, _ARCFACE_DESTINATION)
        aligned = cv2.warpAffine(image, transform, (112, 112), borderValue=0.0)
        blob = cv2.dnn.blobFromImage(
            aligned,
            1.0 / 127.5,
            (112, 112),
            (127.5, 127.5, 127.5),
            swapRB=True,
        )
        self._recognizer.setInput(blob)
        embedding = np.asarray(self._recognizer.forward(), dtype=np.float32).reshape(-1)
        if not np.all(np.isfinite(embedding)):
            raise ValueError("Non-finite ArcFace embedding")
        norm = np.linalg.norm(embedding)
        if norm == 0:
            raise ValueError("Zero-norm ArcFace embedding")
        return embedding / norm


def extract_arcface_embedding(image_path: str | Path, model_root: str | Path, model_name: str = "antelopev2") -> np.ndarray:
    """Extract one embedding; use ``ArcFaceExtractor`` for batch processing.

    The caller must record checkpoint hash, model name, provider and preprocessing
    in its embedding manifest before results are considered scientific evidence.
    """
    return ArcFaceExtractor(model_root, model_name).extract(image_path)
