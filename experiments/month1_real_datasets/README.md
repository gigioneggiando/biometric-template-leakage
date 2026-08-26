# Month 1 real-dataset evidence

Status: **COMPLETED ENGINEERING VALIDATION; NOT A PAPER REPRODUCTION**.

This package consolidates single-template experiments on three real face datasets: LFW, Olivetti faces, and CFP. Six protocol variants test detector/alignment choice, sample size, and frontal/profile views. A separate 64/128/256-bit sweep tests BioHash dimension on LFW and Olivetti. Larger LFW and CFP frontal also use a crossed `3 identity assignments x 3 key seeds x 3 model seeds` sensitivity design with identity-clustered top-1 intervals. Synthetic data is excluded from the scientific evidence.

Across all six protocol variants, the independent unseen-key MLP remained compatible with chance: top-1 ranged from `1.02%` to `11.57%`, with the applicable chance rate ranging from `1.00%` to `12.50%`. No seed rejected chance in descriptive one-sided exact binomial tests (`p >= 0.1205`). In contrast, the fixed-transform calibration reached `51.11%` to `91.00%` top-1, confirming that the extraction, protection, training, and evaluation path can recover signal when the transformation is reusable.

The crossed-seed sensitivity study reached independent-key cell means of `0.81-1.11%` on CFP versus `1.00%` chance and `2.59-3.58%` on larger LFW versus `3.33%` chance. All 54 independent-key run-level clustered intervals included chance. Fixed-transform cell means remained `91.70-94.74%` and `66.54-77.41%`, respectively. Because cells share fixed datasets, this is descriptive sensitivity evidence rather than independent replication or an equivalence test.

The result is a robust negative Month 1 baseline, not the proposed multi-exposure breakthrough. It does not evaluate whether 2/5/10 independently keyed observations amplify leakage.

- `results_summary.csv`: exact aggregate metrics for all protocol variants.
- `dimension_sweep.csv`: independent-key metrics for the 64/128/256-bit sweep.
- `seed_robustness_summary.csv`: four study/condition summaries over split/key cells.
- `seed_robustness_cells.csv`: all 36 split/key cell aggregates.
- `docs/protocols/real_datasets_month1.md`: protocol, provenance, commands, limitations, and interpretation.

Raw images, embeddings, model weights, and detailed per-run artifacts stay gitignored.
