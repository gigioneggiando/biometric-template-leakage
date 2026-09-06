# Draft email to Sani

**Subject:** MOBIO multi-exposure biometric leakage: results and next steps

Dear Sani,

We have completed an identity-disjoint MOBIO study of key-blind linkage from multiple cancelable face templates. With independent per-record BioHash or MLP-Hash keys, one to ten records remain at chance. When a small hidden pool of transforms recurs, however, ten-record top-1 linkage rises to 51-57% for pools of three or four transforms, versus 3.33% chance. The pattern also appears on LFW and with MLP-Hash.

The new controls strengthen the interpretation: shuffling nine of ten same-identity records collapses the attack to chance; revealing transform-slot labels changes accuracy by at most 4.44 points; repeating the identical image under fresh keys remains at chance; and controlled partial projection reuse produces a graded leakage curve, becoming consistently large from 37.5% shared dimensions in our protocol.

This is an independent study, not a reproduction of *Benchmarking of Cancelable Biometrics for Deep Templates*, because the referenced `benchmark_cb` repository is unavailable. We would appreciate your feedback on whether the fresh-key invariance result plus the transform-reuse/correlation boundary is a suitable paper direction, and on the remaining validation priorities.

Best regards,

Gigi and Manish
