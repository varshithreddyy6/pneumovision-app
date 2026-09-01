"""DenseNet121 binary classifier (ImageNet backbone, pneumonia head)."""

from __future__ import annotations

from typing import Optional

import torch
from torch import nn
from torchvision import models


class PneumoVisionNet(nn.Module):
    def __init__(self, pretrained: bool = False, dropout: float = 0.2) -> None:
        super().__init__()
        weights = models.DenseNet121_Weights.IMAGENET1K_V1 if pretrained else None
        self.backbone = models.densenet121(weights=weights)
        in_features = self.backbone.classifier.in_features
        self.head = nn.Sequential(nn.Dropout(p=dropout), nn.Linear(in_features, 1))
        self.backbone.classifier = self.head
        self.gradcam_layer_name = "features.denseblock4"

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.backbone(x)
        if logits.ndim == 1:
            logits = logits.unsqueeze(0)
        return logits

    @torch.no_grad()
    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        self.eval()
        return torch.sigmoid(self.forward(x))

    def freeze_backbone(self) -> None:
        for name, param in self.backbone.named_parameters():
            param.requires_grad = name.startswith("classifier")

    def unfreeze_last_block(self) -> None:
        for param in self.backbone.parameters():
            param.requires_grad = False
        for name, param in self.backbone.named_parameters():
            if any(k in name for k in ("denseblock4", "features.norm5", "classifier")):
                param.requires_grad = True

    def get_gradcam_target(self) -> nn.Module:
        module: nn.Module = self.backbone
        for part in self.gradcam_layer_name.split("."):
            module = getattr(module, part)
        return module


def torch_load(path, map_location=None):
    try:
        return torch.load(path, map_location=map_location, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=map_location)


def load_checkpoint(path, device: Optional[torch.device] = None) -> tuple[PneumoVisionNet, dict]:
    device = device or torch.device("cpu")
    payload = torch_load(path, map_location=device)
    dropout = 0.2
    state = payload
    meta: dict = {}
    if isinstance(payload, dict) and "model_state" in payload:
        meta = {k: v for k, v in payload.items() if k != "model_state"}
        dropout = float(payload.get("dropout", 0.2))
        state = payload["model_state"]
    model = PneumoVisionNet(pretrained=False, dropout=dropout)
    model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model, meta
