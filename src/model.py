import torch.nn as nn
from torchvision.models import resnet18


def get_model(num_classes: int = 10) -> nn.Module:
    model = resnet18(weights=None)
    model.conv1 = nn.Conv2d(
        3,
        64,
        kernel_size=3,
        stride=1,
        padding=1,
        bias=False,
    )
    model.maxpool = nn.Identity()

    # Replace the final layer for CIFAR-10's 10 classes.
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model