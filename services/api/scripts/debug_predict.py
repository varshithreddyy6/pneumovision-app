"""Print a real prediction (or a traceback) without the browser.

From services/api with venv active:

    python scripts/debug_predict.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PIL import Image

from app.ml.engine import InferenceEngine, _project_root


def main() -> int:
    engine = InferenceEngine.try_load()
    print("engine:", engine)
    if engine is None:
        print("NO MODEL. Train first: python scripts/train_demo.py")
        return 1
    samples = _project_root() / "data" / "samples"
    paths = sorted(samples.glob("*.png")) if samples.exists() else []
    if not paths:
        print("No PNG in data/samples")
        return 1
    path = paths[0]
    print("image:", path)
    result = engine.predict(Image.open(path))
    print("label:", result.label)
    print("P(pneumonia):", round(result.probability_pneumonia, 4))
    print("P(normal):", round(result.probability_normal, 4))
    print("heatmap bytes:", len(result.heatmap_data_url))
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
