# Month 1 LFW engineering validation

**Documentation checked: 2026-09-18. Historical Month 1 evidence retained.** MOBIO access was subsequently completed on 2026-09-04, and current multi-exposure studies cover MOBIO/LFW/FEI/SCface. The latest [216-endpoint scheme follow-up](../scheme_followup_2026-09-18/README.md) covers MOBIO/FEI only. See the [research package](../../reports/README.md) for the nine-page report and 15 figures; the six-run LFW baseline here has not been rerun or replaced.

Status: **COMPLETED ENGINEERING VALIDATION; NOT A PAPER REPRODUCTION**.

This experiment provided the proposal's single-template baseline while MOBIO authorization was pending. The official `benchmark_cb` source remains unresolved. It uses identity-disjoint funneled LFW, official InsightFace `buffalo_l` embeddings, a local 128-bit BioHash reference, and a single-template MLP under fixed-transform and independent unseen-key conditions.

The primary independent-key result was at chance: top-1 `9.60% +/- 0.98%`, AUROC `0.5139 +/- 0.0188`, and EER `49.13% +/- 3.40%` over three seeds. The fixed-transform calibration reached top-1 `53.11% +/- 2.59%`, showing that the pipeline can learn when the transform is reusable. See `docs/protocols/lfw_month1.md` for protocol, hashes, commands, limitations, and interpretation.

The tracked six-run aggregate is `experiments/month1_lfw/results_summary.csv`.
