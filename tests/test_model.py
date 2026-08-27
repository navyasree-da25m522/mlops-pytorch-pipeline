import torch

from src.model import get_model

def test_model_output_shape():
    model = get_model(num_classes=10)
    model.eval()
    sample_input = torch.randn(2, 3, 32, 32)
    with torch.no_grad():
        output = model(sample_input)
    assert output.shape == (2, 10)