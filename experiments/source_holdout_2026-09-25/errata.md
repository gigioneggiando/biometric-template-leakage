# Holdout audit errata

Post-result audit found that `fresh_keyword_arguments` calls `generate_key` with
the invented names `master_key`, `domain` and `value`. The actual signature is
`generate_key(master_seed, split, index)`, so executing that case would raise
`TypeError`. Its semantic label `fresh` is therefore invalid; the appropriate
analyzer outcome is abstention.

The frozen v1 files and reported gates are not rewritten. Excluding this invalid
case gives 16 decisions and seven abstentions over 23 valid cases: 69.57% coverage,
still below the 75% gate. Selective accuracy remains 100% and false-fresh remains
zero. V2 tests use the real keyword names and require invented names to remain
unresolved.
