Here is the cleaned, **VS Code/GitHub-ready `README.md`**. I fixed the malformed Markdown/code fences and tables while preserving the information from your original file. 

````markdown
# PneumoVision

**Educational / research screening prototype** for binary pneumonia detection from chest X-rays.

> ⚠️ **Important Disclaimer**
>
> This application is an educational/research screening prototype. It is **not a medical device** and must not be used to diagnose, treat, or make clinical decisions. Results require qualified professional interpretation.

PneumoVision is a full-stack workstation where a **React** UI communicates with a **FastAPI** service that runs **DenseNet121** transfer learning and **Grad-CAM** attribution.

The browser never imports PyTorch. Model probability is a network score, not clinical certainty.

**Author:** [**Varshith Reddy**](https://linkedin.com/in/varshithreddyvangeti) · **+91 93930 81415** · [**varshithreddyy6@gmail.com**](mailto:varshithreddyy6@gmail.com) · [**GitHub**](https://github.com/varshithreddyy6)

---

## What the Project Does

The system accepts a frontal chest radiograph in JPEG or PNG format and returns:

- Predicted class: **`NORMAL`** or **`PNEUMONIA`**
- Model probabilities:
  - `P(pneumonia)`
  - `P(normal)`
- An uncertainty flag when the score is near the decision threshold
- Grad-CAM heatmap and overlay
- A persistent medical disclaimer

It is intended for **learning, portfolio demonstration, and research plumbing**, including:

- Dataset validation patterns
- A typed API
- A calm clinical UI
- An honest empty metrics page until a real evaluation exists

A bundled **`train_demo.py`** can train a **synthetic DenseNet121 checkpoint** so the UI can run without downloading the multi-gigabyte Kermany / Guangzhou collection.

These weights demonstrate the pipeline only. They are **not a clinical model**.

---

## Features

| Feature | Behaviour |
|---|---|
| Analyze workstation | Upload JPEG/PNG, hero X-ray viewer, analysis rail |
| DenseNet121 inference | ImageNet backbone, binary head, checkpoint at `artifacts/checkpoints/best.pt` |
| Uncertainty band | If `\|p - 0.5\| < 0.10` → human review recommended |
| Grad-CAM | Heatmap + overlay; if Grad-CAM fails, scores still return |
| Health | `GET /health` reports `model_loaded` |
| Performance page | Empty until real evaluation JSON exists; metrics are never fabricated |
| Explain page | Grad-CAM method and caveats |
| About | Dataset limits, bias, disclaimer, developer contact |
| Tests | pytest for API contract and Vitest for client helper |

### Not Included

The project does **not** claim to provide:

- Regulatory clearance
- DICOM/PACS integration
- Verified hospital patient IDs
- Kermany-trained production metrics
- Use as a diagnostic device

---

## Technologies

| Layer | Stack |
|---|---|
| Frontend | Vite, React 18, TypeScript, Tailwind CSS, React Router |
| Backend | FastAPI, Uvicorn, Pydantic Settings |
| ML | PyTorch, torchvision DenseNet121, Pillow |
| Tests | pytest, Vitest |
| UI | Paper `#F6F5F2`, ink `#1A1A1A`, Newsreader + Inter |

Vite proxies **`/health`** and **`/v1`** to **`127.0.0.1:8000`**, so the browser does not call localhost across origins.

---

## Prerequisites

Before running the project, install:

- **Python 3.11+**
  - Python 3.12 has been tested.
  - On Windows, install from [python.org](https://www.python.org/downloads/).
  - Enable **Add python.exe to PATH** during installation.
  - Turn off Microsoft Store `python.exe` aliases.
- **Node.js 18+**
  - Node.js 20 is recommended.
- **Git**
- Approximately **2 GB of disk space** for PyTorch and ImageNet weights during the first training run.

---

# How to Run Locally

You need **two terminals**.

The API must be running before using the Analyze page.

---

## 1. Clone the Repository

```bash
git clone https://github.com/varshithreddyy6/pneumovision-app.git
cd pneumovision-app
````

---

## 2. Start the Backend

### Windows PowerShell

Open **Terminal 1** and navigate to:

```powershell
cd pneumovision-app\services\api
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Your terminal prompt should start with:

```text
(.venv)
```

Then install the dependencies:

```powershell
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### macOS / Linux

```bash
cd pneumovision-app/services/api
python3 -m venv .venv
source .venv/bin/activate

pip install torch torchvision
pip install -r requirements.txt

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Leave the API process running.

### Backend URLs

Health endpoint:

[http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

OpenAPI documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

> **Troubleshooting**
>
> If you see `No module named uvicorn`, you are probably using the global Python installation or are in the wrong folder.
>
> Activate `.venv` from `services/api`.

---

## 3. Train a Demo Checkpoint

The project requires a checkpoint for inference.

Stop Uvicorn with:

```text
Ctrl+C
```

Make sure you are inside:

```text
services/api
```

and that the virtual environment is active.

Run:

```powershell
python scripts/train_demo.py
```

This creates:

```text
data/samples/
artifacts/checkpoints/best.pt
```

The training process:

* Generates synthetic illustrations
* Trains a DenseNet121-based model
* Downloads DenseNet121 ImageNet weights (~30 MB)
* May take several minutes on CPU

Start Uvicorn again after training.

The health endpoint should now report:

```json
{
  "model_loaded": true
}
```

Without:

```text
artifacts/checkpoints/best.pt
```

the Analyze endpoint returns:

```text
503
```

because the model is not loaded. This is expected.

---

## 4. Start the Frontend

Open **Terminal 2**.

Navigate to the frontend:

### Windows

```powershell
cd pneumovision-app\apps\web
copy .env.example .env
npm install
npm run dev
```

### macOS / Linux

```bash
cd pneumovision-app/apps/web
cp .env.example .env
npm install
npm run dev
```

Keep:

```env
VITE_API_URL=
```

empty so the Vite proxy is used.

Open the application:

[http://localhost:5173/](http://localhost:5173/)

> **Troubleshooting**
>
> If you see `npm ENOENT package.json`, you probably ran the command from the repository root.
>
> `package.json` is located inside:
>
> ```text
> apps/web
> ```

---

## 5. Use Analyze

Upload one of the generated sample images:

```text
data/samples/pneumonia_000.png
```

or:

```text
data/samples/normal_000.png
```

You should see:

* Predicted class
* Percentages
* Grad-CAM heatmap
* Grad-CAM overlay when attribution succeeds

> ⚠️ **Do not upload ID cards, screenshots, or unrelated images.**
>
> These are not chest X-rays, so the model scores on them are meaningless.

---

# Tests

## Backend Tests

From:

```text
services/api
```

with the virtual environment active:

```bash
python -m pytest -q
```

## Frontend Tests

From:

```text
apps/web
```

run:

```bash
npm test
npm run build
```

## Optional Prediction Debugging

Run without the browser:

```bash
python scripts/debug_predict.py
```

This can be useful for debugging prediction-related errors.

---

# API

| Method | Path          | Description                                                       |
| ------ | ------------- | ----------------------------------------------------------------- |
| `GET`  | `/health`     | Returns `status`, `model_loaded`, and `note`                      |
| `GET`  | `/v1/model`   | Returns backbone name and model load status                       |
| `POST` | `/v1/analyze` | Multipart `file` → label, probabilities, and Grad-CAM data URLs   |
| `GET`  | `/v1/metrics` | Returns `{ available: false }` until a real evaluation is written |

### Decision Threshold

The default decision threshold is:

```text
0.50
```

This is a **software default**, not a clinically optimal cut-point.

---

# Project Folder Structure

```text
pneumovision-app/
├── README.md
├── LICENSE                          # MIT
├── .gitignore
├── .env.example
├── docker-compose.yml               # optional
│
├── artifacts/
│   └── checkpoints/
│       └── best.pt                  # gitignored; train locally
│
├── data/
│   └── samples/                     # synthetic PNGs from train_demo.py
│
├── apps/
│   └── web/                         # Vite + React UI
│       ├── package.json
│       ├── vite.config.ts           # proxy /health and /v1 → :8000
│       ├── tailwind.config.js
│       └── src/
│           ├── main.tsx
│           ├── App.tsx
│           ├── index.css
│           ├── components/
│           │   ├── Header
│           │   ├── Footer
│           │   ├── Disclaimer
│           │   └── Layout
│           ├── pages/
│           │   ├── Home
│           │   ├── Analyze
│           │   ├── Performance
│           │   ├── Explain
│           │   └── About
│           └── lib/
│               ├── api.ts            # fetch helpers
│               └── site.ts           # disclaimer + author contact
│
└── services/
    └── api/                         # FastAPI
        ├── requirements.txt
        ├── pytest.ini
        ├── Dockerfile
        ├── app/
        │   ├── main.py              # lifespan loads checkpoint
        │   ├── config.py
        │   ├── schemas.py
        │   ├── state.py
        │   ├── ml/                  # DenseNet121, Grad-CAM, engine
        │   └── routers/             # health, analyze, metrics
        ├── scripts/
        │   ├── train_demo.py
        │   └── debug_predict.py
        └── tests/
            └── test_health.py
```

---

# What Was Worked On

### 1. Product Shell

* Five routes
* Paper-and-ink UI
* Always-on disclaimer
* Author footer

### 2. API Contract

* Health endpoint
* Analyze upload endpoint
* Metrics empty state
* No fabricated AUROC values

### 3. Inference

* DenseNet121 binary head
* Checkpoint loading on process start
* Decision threshold
* Uncertainty band

### 4. Explainability

Grad-CAM is applied to:

```text
features.denseblock4
```

Pillow/NumPy are used for the colormap, so OpenCV is not required during inference.

### 5. Demo Training

The demo trainer uses:

* Procedural lung-field illustrations
* Two-stage transfer learning
* Frozen classifier training
* Fine-tuning of the last dense block

### 6. Development / Debugging

The project includes:

* Vite proxy
* pytest
* Vitest
* Windows virtual environment instructions
* `debug_predict.py` for prediction errors without the browser

---

# Configuration

| Variable             | Where           | Meaning                           |
| -------------------- | --------------- | --------------------------------- |
| `VITE_API_URL`       | `.env`          | Leave empty to use the Vite proxy |
| `CORS_ORIGINS`       | API environment | Defaults to `*` in this prototype |
| `checkpoint_path`    | `app/config.py` | `artifacts/checkpoints/best.pt`   |
| `decision_threshold` | `app/config.py` | Default `0.50`                    |
| `uncertainty_margin` | `app/config.py` | Default `0.10`                    |

Do **not** commit:

```text
.venv/
node_modules/
.env
*.pt
```

These files are gitignored.

---

# Limitations

> ⚠️ **Please read before using this project.**

* **Not a medical device.** There is no prospective validation or regulatory clearance.
* The demo checkpoint is trained on **synthetic drawings**, not Kermany / Guangzhou radiographs.
* Public Kermany patient IDs, if the dataset is used later, are a **filename heuristic**, not a verified hospital table.
* Pediatric source data introduces potential **adult domain shift**.
* Grad-CAM shows where the **network** looked, not where disease is located.
* Corner markers, devices, and other visual features can become shortcuts for the model.
* Model probability is **not calibrated clinical risk**.

To train on real public data, obtain the Kermany collection under **CC BY 4.0**, build a:

```text
metadata.csv
```

and replace:

```text
train_demo.py
```

with a patient-grouped trainer.

> **Do not quote demo AUROC as pneumonia-detection performance.**

---

# GitHub

Initialize the repository:

```bash
git init
git add .
git commit -m "PneumoVision: FastAPI + React pneumonia screening prototype"
```

Connect the GitHub repository:

```bash
git remote add origin https://github.com/varshithreddyy6/pneumovision-app.git
```

Set the main branch:

```bash
git branch -M main
```

Push:

```bash
git push -u origin main
```

---

# License

**MIT**

See:

```text
LICENSE
```

Dataset images are **not redistributed**.

If you use the Kermany dataset, comply with its **CC BY 4.0** requirements.

---

# Contributing

Issues and pull requests are welcome for the **software side** of the project, including:

* UI
* API
* Training scripts
* Testing
* Developer tooling

Do **not** submit claims of clinical accuracy.

Keep the medical disclaimer visible.

Do not fabricate metrics.

### Preferred Local Check Before a PR

Backend:

```bash
cd services/api
python -m pytest -q
```

Frontend:

```bash
cd ../../apps/web
npm test
npm run build
```

---

## Disclaimer

PneumoVision is provided strictly as an **educational and research software prototype**.

It is not intended to diagnose, treat, prevent, or make clinical decisions regarding pneumonia or any other medical condition.

Any model output must be interpreted by a qualified healthcare professional.

```
```
