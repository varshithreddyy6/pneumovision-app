"""Load checkpoint once; predict + Grad-CAM per image."""

from __future__ import annotations

import base64
import io
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image

from app.config import settings

LOGGER = logging.getLogger("pneumovision.engine")


def _project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "apps" / "web").exists() and (parent / "services" / "api").exists():
            return parent
    return here.parents[4]

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def _device():
    import torch

    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def _to_data_url(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def _eval_transform(image: Image.Image, size: int):
    from torchvision import transforms as T

    tfm = T.Compose(
        [
            T.Resize((size, size)),
            T.ToTensor(),
            T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )
    return tfm(image.convert("RGB"))


@dataclass
class InferenceResult:
    label: str
    probability_pneumonia: float
    probability_normal: float
    threshold: float
    uncertain: bool
    review_recommended: bool
    confidence_band: str
    heatmap_data_url: str
    overlay_data_url: str
    untrained: bool = False


class InferenceEngine:
    def __init__(self, model, device, untrained: bool = False) -> None:
        self.model = model
        self.device = device
        self.untrained = untrained
        self.image_size = int(settings.image_size)
        self.threshold = float(settings.decision_threshold)
        self.margin = float(settings.uncertainty_margin)

    @classmethod
    def try_load(cls) -> Optional["InferenceEngine"]:
        try:
            import torch  # noqa: F401
        except ImportError:
            LOGGER.warning("PyTorch is not installed. Inference disabled.")
            return None
        from app.ml.densenet import PneumoVisionNet, load_checkpoint

        device = _device()
        ckpt = Path(settings.checkpoint_path)
        if not ckpt.is_absolute():
            ckpt = _project_root() / ckpt
        if ckpt.exists():
            model, meta = load_checkpoint(ckpt, device=device)
            LOGGER.info("Loaded checkpoint %s (%s)", ckpt, meta.get("model_name", "densenet121"))
            return cls(model, device, untrained=False)
        LOGGER.warning("No checkpoint at %s", ckpt)
        return None

    def predict(self, image: Image.Image) -> InferenceResult:
        import logging

        import torch

        rgb = image.convert("RGB")
        tensor = _eval_transform(rgb, self.image_size).unsqueeze(0).to(self.device)
        with torch.inference_mode():
            prob = float(self.model.predict_proba(tensor).detach().cpu().reshape(-1)[0].item())
        p = min(max(prob, 0.0), 1.0)
        label = "PNEUMONIA" if p >= self.threshold else "NORMAL"
        uncertain = abs(p - self.threshold) < self.margin
        distance = abs(p - self.threshold)
        if self.untrained:
            band = "UNTRAINED MODEL — do not interpret"
            uncertain = True
        elif uncertain:
            band = "near-threshold (human review recommended)"
        elif distance >= 0.35:
            band = "far from threshold"
        else:
            band = "moderately away from threshold"

        heatmap_url = ""
        overlay_url = ""
        try:
            from app.ml.gradcam import GradCAM, heatmap_to_pil, overlay_to_pil

            sized = rgb.resize((self.image_size, self.image_size), Image.Resampling.BILINEAR)
            with GradCAM(self.model) as cam:
                heat = cam.generate(tensor)
            heatmap_url = _to_data_url(heatmap_to_pil(heat))
            overlay_url = _to_data_url(overlay_to_pil(sized, heat))
        except Exception:
            logging.getLogger("pneumovision.engine").exception("Grad-CAM failed; returning scores only")

        return InferenceResult(
            label=label,
            probability_pneumonia=p,
            probability_normal=1.0 - p,
            threshold=self.threshold,
            uncertain=uncertain,
            review_recommended=uncertain,
            confidence_band=band,
            heatmap_data_url=heatmap_url,
            overlay_data_url=overlay_url,
            untrained=self.untrained,
        )
