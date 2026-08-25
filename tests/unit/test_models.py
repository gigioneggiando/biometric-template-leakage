import torch
from biometrics_ai.aggregation.models import DeepSetsExtractor


def test_deepsets_is_permutation_invariant_and_masked():
    torch.manual_seed(1)
    model = DeepSetsExtractor(4, 3)
    values = torch.randn(2, 3, 4)
    mask = torch.tensor([[True, True, False], [True, True, True]])
    assert torch.allclose(model(values, mask), model(values[:, [1, 0, 2]], mask[:, [1, 0, 2]]), atol=1e-6)
