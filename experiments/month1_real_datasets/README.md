# Month 1 real-dataset evidence

Status: **COMPLETED ENGINEERING VALIDATION; NOT A PAPER REPRODUCTION**.

This package consolidates single-template experiments on three real face datasets: LFW, Olivetti faces, and CFP. Six protocol variants test detector/alignment choice, sample size, and frontal/profile views. A separate 64/128/256-bit sweep tests BioHash dimension on LFW and Olivetti. Synthetic data is excluded from the scientific evidence.

Across all six protocol variants, the independent unseen-key MLP remained at chance: top-1 ranged from `1.02%` to `11.57%`, with the applicable chance rate ranging from `1.00%` to `12.50%`. No seed rejected chance in descriptive one-sided exact binomial tests (`p >= 0.1205`). In contrast, the fixed-transform calibration reached `51.11%` to `91.00%` top-1, confirming that the extraction, protection, training, and evaluation path can recover signal when the transformation is reusable.

The result is a robust negative Month 1 baseline, not the proposed multi-exposure breakthrough. It does not evaluate whether 2/5/10 independently keyed observations amplify leakage.

- `results_summary.csv`: exact aggregate metrics for all protocol variants.
- `dimension_sweep.csv`: independent-key metrics for the 64/128/256-bit sweep.
- `docs/protocols/real_datasets_month1.md`: protocol, provenance, commands, limitations, and interpretation.

Raw images, embeddings, model weights, and detailed per-run artifacts stay gitignored.
