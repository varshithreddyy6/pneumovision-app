# PneumoVision — full-stack foundation

Minimal product shell for an educational pneumonia screening prototype.

This is **scaffolding only**: layout, design tokens, five routes, and a FastAPI contract. There is no trained model, no Grad-CAM compute, and no metrics. That is intentional.

> This application is an educational/research screening prototype. It is not a medical device and must not be used to diagnose, treat, or make clinical decisions. Results require qualified professional interpretation.

**Author:** [Varshith Reddy](https://linkedin.com/in/varshithreddyvangeti) · [+91 93930 81415](tel:+919393081415) · [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com) · [GitHub](https://github.com/varshithreddyy6)

---

## Stack

| Layer | Choice |
| --- | --- |
| Frontend | Vite · React 18 · TypeScript · Tailwind CSS · React Router |
| Backend | FastAPI · Uvicorn · Pydantic |
| UI | Paper `#F6F5F2`, ink `#1A1A1A`, Newsreader + Inter, 1px rules, no shadows |

---

## Folder structure

```text
pneumovision-app/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml          # optional
├── apps/
│   └── web/                    # React SPA
│       ├── index.html
│       ├── package.json
│       ├── vite.config.ts
│       ├── tailwind.config.js
│       └── src/
│           ├── main.tsx
│           ├── App.tsx
│           ├── index.css
│           ├── components/     # Header, Footer, Disclaimer, Layout
│           ├── pages/          # Home, Analyze, Performance, Explain, About
│           └── lib/            # api.ts, site.ts (contact + disclaimer)
└── services/
    └── api/                    # FastAPI
        ├── requirements.txt
        ├── pytest.ini
        ├── Dockerfile
        ├── app/
        │   ├── main.py
        │   ├── config.py
        │   ├── schemas.py
        │   └── routers/        # health, analyze, metrics
        └── tests/
            └── test_health.py
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+ (20 recommended)
- Git

---

## 1. Clone / open in VS Code

```bash
git clone https://github.com/varshithreddyy6/pneumovision-app.git
cd pneumovision-app
code .
```

If this is a new repo on your machine:

```bash
cd pneumovision-app
git init
git add .
git commit -m "Initial foundation: FastAPI + React scaffold"
```

---

## 2. Backend

```bash
cd services/api
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Check:

- Health: http://localhost:8000/health
- OpenAPI: http://localhost:8000/docs

---

## 3. Frontend

Open a **second** terminal:

```bash
cd apps/web
cp .env.example .env          # leave VITE_API_URL empty — Vite proxies /v1 to :8000
npm install
npm run dev
```

Open http://localhost:5173

---

## 4. Test

Backend (from `services/api` with venv active):

```bash
pytest
```

Frontend (from `apps/web`):

```bash
npm test
npm run build
```

Manual smoke:

1. Home loads serif title + three columns.
2. Footer shows **VARSHITH REDDY**, phone, email, LinkedIn, GitHub.
3. Disclaimer strip is on every page.
4. Analyze → choose a PNG → Run analysis → status `not_implemented` (expected).
5. Performance shows em dashes, not fake AUROC.

---

## 5. Push to GitHub

```bash
git remote add origin https://github.com/varshithreddyy6/pneumovision-app.git
git branch -M main
git push -u origin main
```

Do not commit `.venv/`, `node_modules/`, `.env`, or model weights. They are already in `.gitignore`.

---

## API contract (stubs)

| Method | Path | Today |
| --- | --- | --- |
| GET | `/health` | `{ status: "ok", model_loaded: false }` |
| GET | `/v1/model` | Scaffold note |
| POST | `/v1/analyze` | Accepts JPEG/PNG, **does not infer** |
| GET | `/v1/metrics` | `{ available: false }` |

Wire `Predictor` inside `services/api/app/routers/analyze.py` when you are ready. Do not invent metrics in `metrics.py`.

---

## UI notes

Inspired by quiet editorial / paper interfaces (generous whitespace, thin rules, one ink color, serif headlines). Red and motion are unused in this foundation. The X-ray frame is a dark rectangle so a film will sit as the hero later.

Developer contact is in **every footer** and on **About**.

---

## Make pneumonia detection actually run

The UI is only a shell until a **checkpoint** exists at
`artifacts/checkpoints/best.pt`.

From `services/api` with the venv **active**:

```powershell
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python scripts/train_demo.py
```

First run downloads ImageNet DenseNet121 (~30 MB) and trains for a few minutes
on CPU. Then **stop uvicorn (Ctrl+C) and start it again** so it loads `best.pt`.

Check http://127.0.0.1:8000/health — `"model_loaded": true`.

On Analyze, use `data/samples/pneumonia_000.png` or `normal_000.png` (created by
the trainer). A voter ID is not an X-ray; scores on it mean nothing.

This demo is trained on **synthetic drawings**, not Kermany hospital films. It
proves the pipeline. It is not a clinical model.

---

## What this repo is not

- Not a medical device
- Not a trained DenseNet
- Not Streamlit
- Not a completed product

Next implementation slice: load a checkpoint in the API lifespan and fill the analysis rail + Grad-CAM row.
