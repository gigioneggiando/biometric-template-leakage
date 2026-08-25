"""Extract ArcFace embeddings from a CSV manifest after model/dataset authorization."""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import numpy as np
from biometrics_ai.face import extract_arcface_embedding


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True, type=Path, help="CSV with sample_id,identity_id,source_image,split")
    parser.add_argument("--model-root", required=True, type=Path)
    parser.add_argument("--model-name", default="antelopev2")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.input_csv.open(encoding="utf-8", newline="")))
    vectors, metadata = [], []
    for row in rows:
        vector = extract_arcface_embedding(row["source_image"], args.model_root, args.model_name)
        vectors.append(vector)
        metadata.append({**row, "embedding_model": args.model_name, "dimension": len(vector), "preprocessing_version": "insightface_faceanalysis_640_largest_face"})
    args.output.mkdir(parents=True, exist_ok=True)
    np.save(args.output / "embeddings.npy", np.stack(vectors))
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (args.output / "embedding_manifest.json").write_text(json.dumps({"model": args.model_name, "model_root": str(args.model_root), "input_manifest_sha256": file_hash(args.input_csv), "count": len(vectors)}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
