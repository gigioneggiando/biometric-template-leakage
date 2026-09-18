# Natural-norm and native-matching audit

Protocol written on 2026-09-18 before inspecting new raw-embedding or control results. This is a user-authorized revision study, not a retroactive preregistration of the existing 216 endpoints. Maximum new execution budget: 3,600 seconds on local CPU; stop and report incomplete cells rather than silently expanding it. No acquisition, credentials, face-model training or new dataset is authorized by this protocol.

## Questions and fixed comparisons

1. Does the local PolyProtect polynomial evaluation agree with a separately written scalar reference across overlaps, padding and raw/unit input scales? Does IoM-GRP agree with explicit grouped dot-product argmax? These are independent computational paths, not independent human review or source-exact certification.
2. Does genuine pre-normalization ArcFace magnitude carry identity information on available MOBIO/FEI records? Re-extract from authorized source images with the existing YuNet/ArcFace checkpoint and preprocessing. Require recovered normalized vectors to agree with saved vectors (maximum absolute deviation <= 1e-4); preserve failures, record counts and hashes. Never reconstruct natural norms by assigning arbitrary scales to normalized embeddings.
3. Compare direct native matching using unit inputs, raw inputs, and raw directions with norms permuted across records within each split. Permutation preserves the empirical norm distribution but breaks its person/record association. Add a fixed-radius arm at the median training norm to distinguish overall scale from individual norm information. Use identical fresh keys across input arms.
4. Audit the fresh PolyProtect result with a separately evaluated polynomial transform and an independently computed cosine-distance ranking; check gallery/probe exclusion, unique source records, key uniqueness, zero/nonfinite templates, score ties and dependence on gallery order. Add a linear-term-only PolyProtect diagnostic to investigate low-order dominance; this is a post-pilot mechanism diagnostic, not a new security theorem.

## Evaluation

Use identity assignments 91831/91843 and native key seeds 91873/91879/91883, matching the prior follow-up. One held-out gallery record per test identity, all remaining records as probes; equal weight per identity. Compare norms alone by nearest absolute log-norm distance to gallery norms. No identity labels enter the protection or matcher. Norm-shuffle seed 91901; analysis seed 91903; 4,999 gallery-label permutations; 4,000 identity bootstrap draws. Keep identity-level data private.

Primary native family: unit/raw/shuffled/fixed-radius PolyProtect above the gallery-label null in 2 datasets x 2 partitions x 4 arms, averaging three fixed key seeds before permutation (16 hypotheses). Norm-only family: four dataset/partition tests. Paired raw-minus-unit and raw-minus-shuffled native gains form a separate family of eight two-sided identity sign-flip tests with paired identity-bootstrap intervals. Adjust each planned family with Holm; unavailable tests count toward the planned family size. Native intervals condition on the fixed key ensemble and overlapping partitions, not independent populations. Additional mechanism and implementation checks are descriptive.

## Existing-run statistical revision

Reuse retained private identity scores from the 216 trained endpoints; do not retrain merely to produce different p-values. Export crossed model-seed/identity intervals, all mean/DeepSets ten-minus-one contrasts, model-seed ranges and leave-one-seed-out gain checks. Preserve the original eight-hypothesis primary analysis unchanged. A separate post-hoc family over all available contrasts is exploratory and must be labelled as such. Report failed/negative gains and chance-compatible intervals, not just successes. No equivalence claim or margin selected from these results.

## Scope and provenance

Freeze source/configuration/protocol hashes before execution; save only compact aggregates, model/input digests, counts and diagnostic discrepancies publicly. Private raw embeddings and per-identity values stay under ignored results. No raw image, identity label, key or personal source path belongs in tracked outputs. If source images are unavailable or normalization agreement fails, mark the natural-norm experiment blocked and do not substitute synthetic radial stress. New learned raw-input training is not necessary for the native/norm-only questions and is not implied by their completion. Full cross-dataset attacker confirmation and independent review remain separate.