"""Extract ArcFace embeddings from a CSV manifest after model/dataset authorization."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import numpy as np
from biometrics_ai.face import ArcFaceExtractor, OpenCvArcFaceExtractor, OpenCvYuNetArcFaceExtractor


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True, type=Path, help="CSV with sample_id,identity_id,source_image,split")
    parser.add_argument("--backend", choices=("insightface", "opencv", "opencv-yunet"), default="insightface")
    parser.add_argument("--model-root", type=Path)
    parser.add_argument("--model-name", default="antelopev2")
    parser.add_argument("--recognition-model", type=Path)
    parser.add_argument("--detection-model", type=Path)
    parser.add_argument("--detection-threshold", type=float, default=0.5)
    parser.add_argument("--skip-errors", action="store_true")
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.input_csv.open(encoding="utf-8", newline="")))
    model_files: dict[str, dict[str, str]] = {}
    if args.backend == "insightface":
        if args.model_root is None:
            parser.error("--model-root is required for the insightface backend")
        extractor = ArcFaceExtractor(args.model_root, args.model_name)
        preprocessing_version = "insightface_faceanalysis_640_largest_face"
    else:
        if args.recognition_model is None or args.detection_model is None:
            parser.error("--recognition-model and --detection-model are required for the opencv backend")
        if args.model_name == "antelopev2":
            # The OpenCV backend receives a checkpoint directly rather than an
            # InsightFace model pack, so record the actual checkpoint filename.
            args.model_name = args.recognition_model.stem
        if args.backend == "opencv":
            extractor = OpenCvArcFaceExtractor(
                args.recognition_model,
                args.detection_model,
                detection_threshold=args.detection_threshold,
            )
            preprocessing_version = "opencv_scrfd_640_arcface_5point_v1"
        else:
            extractor = OpenCvYuNetArcFaceExtractor(
                args.recognition_model,
                args.detection_model,
                detection_threshold=args.detection_threshold,
            )
            preprocessing_version = "opencv_yunet_native_arcface_5point_v1"
        model_files = {
            "recognition": {"path": args.recognition_model.as_posix(), "sha256": file_hash(args.recognition_model)},
            "detection": {"path": args.detection_model.as_posix(), "sha256": file_hash(args.detection_model)},
        }

    vectors, metadata, failures = [], [], []
    for index, row in enumerate(rows, start=1):
        try:
            vector = extractor.extract(row["source_image"])
        except Exception as error:
            if not args.skip_errors:
                raise
            failures.append({"sample_id": row.get("sample_id"), "error": f"{type(error).__name__}: {error}"})
            continue
        vectors.append(vector)
        metadata.append({**row, "embedding_model": args.model_name, "dimension": len(vector), "preprocessing_version": preprocessing_version})
        if args.progress_every > 0 and index % args.progress_every == 0:
            print(f"Processed {index}/{len(rows)} images; failures={len(failures)}", flush=True)
    if not vectors:
        raise SystemExit("No embeddings were extracted")
    args.output.mkdir(parents=True, exist_ok=True)
    np.save(args.output / "embeddings.npy", np.stack(vectors))
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (args.output / "failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
    manifest = {
        "model": args.model_name,
        "backend": args.backend,
        "model_root": str(args.model_root) if args.model_root else None,
        "model_files": model_files,
        "input_manifest_sha256": file_hash(args.input_csv),
        "count": len(vectors),
        "failure_count": len(failures),
        "preprocessing_version": preprocessing_version,
    }
    (args.output / "embedding_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
