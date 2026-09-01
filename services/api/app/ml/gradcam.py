"""Grad-CAM for DenseNet121. No OpenCV — Pillow + NumPy only (Windows-friendly)."""

from __future__ import annotations

from typing import Optional

import numpy as np
import torch
from PIL import Image
from torch import nn


class GradCAM:
    def __init__(self, model: nn.Module, target_layer: Optional[nn.Module] = None) -> None:
        self.model = model
        self.model.eval()
        if target_layer is None:
            target_layer = model.get_gradcam_target()
        self.target_layer = target_layer
        self._activations: Optional[torch.Tensor] = None
        self._gradients: Optional[torch.Tensor] = None
        self._handles = [self.target_layer.register_forward_hook(self._on_forward)]

    def _on_forward(self, module, inputs, output):  # noqa: ANN001
        if not torch.is_tensor(output):
            return None
        captured = output.clone()
        self._activations = captured.detach()

        def _save_grad(grad: torch.Tensor) -> None:
            self._gradients = grad.detach()

        captured.register_hook(_save_grad)
        return captured

    def close(self) -> None:
        for handle in self._handles:
            handle.remove()
        self._handles = []

    def __enter__(self) -> "GradCAM":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        self.close()

    def generate(self, input_tensor: torch.Tensor) -> np.ndarray:
        if input_tensor.ndim == 3:
            input_tensor = input_tensor.unsqueeze(0)
        device = next(self.model.parameters()).device
        x = input_tensor.to(device)
        with torch.enable_grad():
            x = x.detach().requires_grad_(True)
            self.model.zero_grad(set_to_none=True)
            logits = self.model(x)
            if logits.ndim == 1:
                logits = logits.unsqueeze(0)
            logits[:, 0].sum().backward()
        if self._activations is None or self._gradients is None:
            raise RuntimeError("Grad-CAM hooks did not capture activations.")
        weights = self._gradients.mean(dim=(2, 3), keepdim=True)
        cam = torch.relu((weights * self._activations).sum(dim=1)[0])
        cam_min, cam_max = cam.min(), cam.max()
        if (cam_max - cam_min) > 1e-8:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = torch.zeros_like(cam)
        h, w = int(x.shape[-2]), int(x.shape[-1])
        small = cam.detach().cpu().numpy().astype(np.float32)
        heat = np.array(
            Image.fromarray((np.clip(small, 0, 1) * 255).astype(np.uint8), mode="L").resize(
                (w, h), Image.Resampling.BILINEAR
            ),
            dtype=np.float32,
        ) / 255.0
        return np.clip(heat, 0.0, 1.0)


def _jet(gray: np.ndarray) -> np.ndarray:
    x = np.clip(gray, 0.0, 1.0)
    r = np.clip(1.5 - np.abs(4 * x - 3), 0, 1)
    g = np.clip(1.5 - np.abs(4 * x - 2), 0, 1)
    b = np.clip(1.5 - np.abs(4 * x - 1), 0, 1)
    return (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)


def heatmap_to_pil(heatmap: np.ndarray) -> Image.Image:
    return Image.fromarray(_jet(np.asarray(heatmap, dtype=np.float32)), mode="RGB")


def overlay_to_pil(image: Image.Image, heatmap: np.ndarray, alpha: float = 0.40) -> Image.Image:
    rgb = np.array(image.convert("RGB"), dtype=np.float32)
    heat = np.asarray(heatmap, dtype=np.float32)
    if heat.shape[:2] != rgb.shape[:2]:
        heat = np.array(
            Image.fromarray((np.clip(heat, 0, 1) * 255).astype(np.uint8), mode="L").resize(
                (rgb.shape[1], rgb.shape[0]), Image.Resampling.BILINEAR
            ),
            dtype=np.float32,
        ) / 255.0
    colored = _jet(heat).astype(np.float32)
    out = np.clip(rgb * (1.0 - alpha) + colored * alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
