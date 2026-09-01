#!/usr/bin/env python3
"""Train a demo DenseNet121 on synthetic chest-like images and save best.pt.

This is a pipeline check, NOT clinical training.
Run from services/api with the venv active:

    python scripts/train_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_API = Path(__file__).resolve().parents[1]
if str(ROOT_API) not in sys.path:
    sys.path.insert(0, str(ROOT_API))

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms as T
from tqdm import tqdm

from app.ml.densenet import PneumoVisionNet

PROJECT = ROOT_API.parents[1]  # pneumovision-app
CKPT = PROJECT / "artifacts" / "checkpoints" / "best.pt"
SAMPLES = PROJECT / "data" / "samples"
SIZE = 224
SEED = 42
BATCH = 8
STAGE1 = 3
STAGE2 = 2


def synthesize(rng: np.random.Generator, pneumonia: bool, size: int = SIZE) -> Image.Image:
    h = w = size
    base = rng.normal(loc=28, scale=6, size=(h, w)).clip(0, 255)
    yy, xx = np.mgrid[0:h, 0:w]
    cy, cx = h * 0.52, w * 0.50
    mediastinum = np.exp(-((xx - cx) ** 2) / (2 * (w * 0.10) ** 2) - ((yy - cy) ** 2) / (2 * (h * 0.28) ** 2))
    heart = np.exp(
        -((xx - (cx + w * 0.07)) ** 2) / (2 * (w * 0.16) ** 2)
        - ((yy - (cy + h * 0.08)) ** 2) / (2 * (h * 0.18) ** 2)
    )
    left = np.exp(-((xx - w * 0.32) ** 2) / (2 * (w * 0.16) ** 2) - ((yy - h * 0.50) ** 2) / (2 * (h * 0.24) ** 2))
    right = np.exp(-((xx - w * 0.68) ** 2) / (2 * (w * 0.16) ** 2) - ((yy - h * 0.50) ** 2) / (2 * (h * 0.24) ** 2))
    img = base + 70 * mediastinum + 90 * heart - 55 * left - 55 * right
    if pneumonia:
        ox = w * (0.32 if rng.random() < 0.5 else 0.68)
        oy = h * rng.uniform(0.42, 0.62)
        blob = np.exp(
            -((xx - ox) ** 2) / (2 * (w * 0.09) ** 2) - ((yy - oy) ** 2) / (2 * (h * 0.10) ** 2)
        )
        img = img + 85 * blob
    img = np.clip(img + rng.normal(0, 4, size=(h, w)), 0, 255).astype(np.uint8)
    pil = Image.fromarray(img, mode="L").convert("RGB")
    draw = ImageDraw.Draw(pil)
    draw.line([(w * 0.50, h * 0.16), (w * 0.50, h * 0.88)], fill=150, width=3)
    return pil.filter(ImageFilter.GaussianBlur(radius=0.8))


class DemoSet(Dataset):
    def __init__(self, items: list[tuple[Path, int]], train: bool) -> None:
        mean, std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
        if train:
            self.tfm = T.Compose(
                [
                    T.Resize((SIZE, SIZE)),
                    T.RandomHorizontalFlip(),
                    T.RandomAffine(degrees=8, translate=(0.04, 0.04)),
                    T.ToTensor(),
                    T.Normalize(mean, std),
                ]
            )
        else:
            self.tfm = T.Compose(
                [T.Resize((SIZE, SIZE)), T.ToTensor(), T.Normalize(mean, std)]
            )
        self.items = items

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, i: int):
        path, y = self.items[i]
        img = Image.open(path).convert("RGB")
        return self.tfm(img), torch.tensor([y], dtype=torch.float32)


def main() -> int:
    rng = np.random.default_rng(SEED)
    SAMPLES.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[Path, int]] = []
    print("Generating 48 synthetic illustrations (not real radiographs)...")
    for i in range(24):
        p = SAMPLES / f"normal_{i:03d}.png"
        synthesize(rng, pneumonia=False).save(p)
        rows.append((p, 0))
    for i in range(24):
        p = SAMPLES / f"pneumonia_{i:03d}.png"
        synthesize(rng, pneumonia=True).save(p)
        rows.append((p, 1))

    rng.shuffle(rows)
    split = int(0.8 * len(rows))
    train_rows, val_rows = rows[:split], rows[split:]
    train_loader = DataLoader(DemoSet(train_rows, True), batch_size=BATCH, shuffle=True)
    val_loader = DataLoader(DemoSet(val_rows, False), batch_size=BATCH)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)
    print("Downloading ImageNet DenseNet121 weights if needed...")
    model = PneumoVisionNet(pretrained=True, dropout=0.2).to(device)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    def run_epoch(train: bool) -> float:
        model.train(train)
        total, n = 0.0, 0
        loader = train_loader if train else val_loader
        for x, y in tqdm(loader, leave=False):
            x, y = x.to(device), y.to(device)
            if train:
                opt.zero_grad(set_to_none=True)
            logits = model(x)
            loss = loss_fn(logits, y)
            if train:
                loss.backward()
                opt.step()
            total += float(loss.item()) * x.size(0)
            n += x.size(0)
        return total / max(n, 1)

    best = 1e9
    CKPT.parent.mkdir(parents=True, exist_ok=True)

    model.freeze_backbone()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    print("Stage 1 — train classifier")
    for epoch in range(1, STAGE1 + 1):
        tr, va = run_epoch(True), run_epoch(False)
        print(f"  epoch {epoch} train {tr:.4f} val {va:.4f}")
        if va < best:
            best = va
            torch.save(
                {"model_state": model.state_dict(), "model_name": "densenet121", "dropout": 0.2},
                CKPT,
            )

    model.unfreeze_last_block()
    payload = torch.load(CKPT, map_location=device, weights_only=False)
    model.load_state_dict(payload["model_state"])
    model.unfreeze_last_block()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-5)
    print("Stage 2 — fine-tune last block")
    for epoch in range(1, STAGE2 + 1):
        tr, va = run_epoch(True), run_epoch(False)
        print(f"  epoch {epoch} train {tr:.4f} val {va:.4f}")
        if va < best:
            best = va
            torch.save(
                {"model_state": model.state_dict(), "model_name": "densenet121", "dropout": 0.2},
                CKPT,
            )

    print(f"Saved {CKPT}")
    print("Restart uvicorn, then open Analyze and upload data/samples/pneumonia_000.png")
    print("WARNING: synthetic demo weights. Not a clinical model.")
    return 0


if __name__ == "__main__":
    try:
        from tqdm import tqdm  # noqa: F401
    except ImportError:
        print("pip install tqdm")
        raise
    raise SystemExit(main())
