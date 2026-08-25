"""Optional InsightFace-backed ArcFace extraction with explicit model provenance."""
from __future__ import annotations
from pathlib import Path
import numpy as np


def extract_arcface_embedding(image_path: str | Path, model_root: str | Path, model_name: str = "antelopev2") -> np.ndarray:
    """Extract the largest detected face embedding; weights must be acquired lawfully.

    The caller must record checkpoint hash, model name, provider and preprocessing
    in its embedding manifest before results are considered scientific evidence.
    """
    try:
        from insightface.app import FaceAnalysis
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("Install optional face dependencies: python -m pip install -e '.[face]'") from error
    image = np.asarray(Image.open(image_path).convert("RGB"))[:, :, ::-1]
    app = FaceAnalysis(name=model_name, root=str(model_root), providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(image)
    if not faces:
        raise ValueError(f"No face detected in {image_path}")
    face = max(faces, key=lambda value: (value.bbox[2] - value.bbox[0]) * (value.bbox[3] - value.bbox[1]))
    embedding = np.asarray(face.embedding, dtype=np.float32)
    if not np.all(np.isfinite(embedding)):
        raise ValueError("Non-finite ArcFace embedding")
    return embedding / np.linalg.norm(embedding)
