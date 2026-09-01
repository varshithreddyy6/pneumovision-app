# PneumoVision

**PneumoVision** is a full-stack educational and research screening prototype for binary pneumonia detection from chest X-ray images.

The project combines a **React + TypeScript frontend**, a **FastAPI backend**, and a **PyTorch DenseNet121 machine-learning pipeline** with **Grad-CAM explainability**. Users can upload a supported chest X-ray image, send it to the backend for inference, receive a model prediction, view probability scores, and inspect a Grad-CAM visualization when attribution succeeds.

> ⚠️ **Medical Disclaimer**
>
> PneumoVision is an educational/research software prototype. It is **not a medical device** and must not be used to diagnose, treat, prevent, or make clinical decisions. Any model output requires interpretation by a qualified healthcare professional.
>
> The included demo checkpoint is trained on synthetic illustrations and must **not** be interpreted as a clinically validated pneumonia-detection model.

---

## Table of Contents

* [Project Overview](#project-overview)
* [What the Project Does](#what-the-project-does)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Application Architecture](#application-architecture)
* [Project Folder Structure](#project-folder-structure)
* [Prerequisites](#prerequisites)
* [Running the Project Locally](#running-the-project-locally)
* [API Endpoints](#api-endpoints)
* [Machine Learning Pipeline](#machine-learning-pipeline)
* [Grad-CAM Explainability](#grad-cam-explainability)
* [Configuration](#configuration)
* [Testing](#testing)
* [Development and Debugging](#development-and-debugging)
* [Demo Data and Model Files](#demo-data-and-model-files)
* [What Was Worked On](#what-was-worked-on)
* [Design and UI](#design-and-ui)
* [Limitations](#limitations)
* [Responsible Use](#responsible-use)
* [Docker](#docker)
* [Future Improvements](#future-improvements)
* [Contributing](#contributing)
* [License](#license)
* [Author](#author)

---

# Project Overview

PneumoVision demonstrates how a machine-learning workflow can be integrated into a complete software product instead of remaining limited to a notebook or isolated model script.

The application provides a frontend workstation where users can upload an image and interact with the model through a FastAPI service.

The project includes:

* React-based web interface
* TypeScript frontend
* FastAPI REST API
* DenseNet121-based image classification
* Grad-CAM attribution
* Demo training pipeline
* Synthetic sample images
* Model health/status endpoints
* Frontend and backend tests
* Local environment configuration
* Optional/experimental Docker configuration
* Persistent medical disclaimer
* Performance page designed to avoid fabricated metrics

The browser does not directly import PyTorch. Machine-learning processing is handled by the Python backend.

---

# What the Project Does

The system accepts a frontal chest radiograph in **JPEG or PNG** format.

The analysis workflow can provide:

* Predicted class:

  * `NORMAL`
  * `PNEUMONIA`
* Model probability for pneumonia
* Model probability for normal
* An uncertainty indication around the decision threshold
* Grad-CAM heatmap information
* Grad-CAM overlay when attribution succeeds

The project is intended for:

* Education
* Portfolio demonstration
* Full-stack machine-learning development
* Computer-vision experimentation
* Explainable-AI experimentation
* Research software prototyping
* API/frontend integration practice

The project deliberately avoids claiming clinical performance that has not been established through a real evaluation pipeline.

---

# Features

## 1. Chest X-Ray Upload

The Analyze page allows users to upload supported image files.

Supported image formats include:

* JPEG
* PNG

The image is sent to the FastAPI backend for validation and inference.

---

## 2. Binary Pneumonia Classification

The application uses a DenseNet121-based image classification pipeline to produce one of two classes:

```text
NORMAL
PNEUMONIA
```

---

## 3. Probability Scores

The backend returns model probability information associated with the prediction.

These probabilities represent neural-network output and should not be interpreted as calibrated clinical risk.

---

## 4. Uncertainty Band

PneumoVision includes a software-level uncertainty indication around the classification threshold.

The default values are:

```text
Decision threshold: 0.50
Uncertainty margin: 0.10
```

Predictions close to the decision threshold can be marked for additional human review.

This threshold is a software configuration and is **not a clinically validated confidence boundary**.

---

## 5. Grad-CAM Explainability

The project provides Grad-CAM attribution to visualize image regions that contributed to the model output.

The current implementation targets:

```text
features.denseblock4
```

The resulting heatmap/overlay is intended to help understand model behavior.

It must not be interpreted as a confirmed lesion map or medically verified disease localization.

---

## 6. Health Endpoint

The backend provides:

```http
GET /health
```

This endpoint reports backend health and whether the model is loaded.

---

## 7. Model Information Endpoint

The backend provides:

```http
GET /v1/model
```

This exposes model/backbone information and loading status.

---

## 8. Image Analysis Endpoint

The backend provides:

```http
POST /v1/analyze
```

This endpoint accepts a multipart image upload and performs inference when a valid model checkpoint is available.

---

## 9. Metrics Endpoint

The backend provides:

```http
GET /v1/metrics
```

The project intentionally avoids fabricating machine-learning performance numbers.

Until a real evaluation dataset and reproducible evaluation pipeline are available, the metrics page remains an empty state.

---

## 10. Demo Training Pipeline

The project includes:

```text
services/api/scripts/train_demo.py
```

The script generates synthetic illustrations and trains a demonstration DenseNet121 model.

This allows the complete software pipeline to be exercised without requiring the user to download and redistribute a large medical imaging dataset.

---

## 11. Prediction Debugging

The repository includes:

```text
services/api/scripts/debug_predict.py
```

This allows prediction-related issues to be investigated without using the browser interface.

---

## 12. Automated Testing

The project includes:

* `pytest` for backend tests
* `Vitest` for frontend tests
* Production frontend build validation

---

## 13. Responsive Clinical-Style UI

The frontend uses a clean and restrained visual language intended to resemble a focused workstation rather than a generic machine-learning demo.

---

# Technology Stack

| Area             | Technology              |
| ---------------- | ----------------------- |
| Frontend         | React 18                |
| Language         | TypeScript              |
| Build Tool       | Vite                    |
| Styling          | Tailwind CSS            |
| Routing          | React Router            |
| Backend          | FastAPI                 |
| ASGI Server      | Uvicorn                 |
| Configuration    | Pydantic Settings       |
| Deep Learning    | PyTorch                 |
| Vision           | torchvision             |
| Model            | DenseNet121             |
| Image Processing | Pillow                  |
| Explainability   | Grad-CAM                |
| Backend Testing  | pytest                  |
| Frontend Testing | Vitest                  |
| Containers       | Docker / Docker Compose |

---

# Application Architecture

```text
                         PneumoVision
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        React + TypeScript            FastAPI Backend
        Vite + Tailwind                     │
                │                           │
                │       HTTP / REST         │
                └──────────────────────────►│
                                            │
                                            ▼
                                      Image Validation
                                            │
                                            ▼
                                       Preprocessing
                                            │
                                            ▼
                                        DenseNet121
                                            │
                                  ┌─────────┴─────────┐
                                  │                   │
                                  ▼                   ▼
                              Prediction           Grad-CAM
                                  │                   │
                                  └─────────┬─────────┘
                                            │
                                            ▼
                                       API Response
                                            │
                                            ▼
                                         React UI
```

The frontend communicates with the backend through HTTP APIs.

PyTorch and the machine-learning pipeline remain on the backend.

---

# Project Folder Structure

```text
pneumovision-app/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── apps/
│   └── web/
│       ├── index.html
│       ├── package.json
│       ├── package-lock.json
│       ├── postcss.config.js
│       ├── tailwind.config.js
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       ├── vite.config.ts
│       │
│       ├── public/
│       │   └── favicon.svg
│       │
│       └── src/
│           ├── main.tsx
│           ├── App.tsx
│           ├── index.css
│           │
│           ├── components/
│           │   ├── Header.tsx
│           │   ├── Footer.tsx
│           │   ├── Disclaimer.tsx
│           │   └── Layout.tsx
│           │
│           ├── pages/
│           │   ├── Home.tsx
│           │   ├── Analyze.tsx
│           │   ├── Performance.tsx
│           │   ├── Explain.tsx
│           │   └── About.tsx
│           │
│           └── lib/
│               ├── api.ts
│               ├── api.test.ts
│               └── site.ts
│
├── data/
│   └── samples/
│       ├── normal_000.png
│       ├── normal_001.png
│       ├── ...
│       ├── pneumonia_000.png
│       ├── pneumonia_001.png
│       └── ...
│
└── services/
    └── api/
        ├── Dockerfile
        ├── requirements.txt
        ├── pytest.ini
        │
        ├── app/
        │   ├── __init__.py
        │   ├── main.py
        │   ├── config.py
        │   ├── schemas.py
        │   ├── state.py
        │   │
        │   ├── ml/
        │   │   ├── __init__.py
        │   │   ├── densenet.py
        │   │   ├── engine.py
        │   │   └── gradcam.py
        │   │
        │   └── routers/
        │       ├── __init__.py
        │       ├── analyze.py
        │       ├── health.py
        │       └── metrics.py
        │
        ├── scripts/
        │   ├── train_demo.py
        │   └── debug_predict.py
        │
        └── tests/
            └── test_health.py
```

## Key Directories

### `apps/web/`

Contains the complete React frontend.

Responsibilities include:

* User interface
* Application routing
* API communication
* UI components
* Styling
* Frontend testing

### `services/api/`

Contains the FastAPI backend.

Responsibilities include:

* API routes
* Image validation
* Model management
* Machine-learning inference
* Grad-CAM processing
* Backend testing

### `services/api/app/ml/`

Contains the ML implementation:

```text
densenet.py
engine.py
gradcam.py
```

These modules handle the DenseNet121 model, inference flow, and Grad-CAM functionality.

### `services/api/app/routers/`

Contains the API route modules:

```text
health.py
analyze.py
metrics.py
```

### `services/api/scripts/`

Contains development utilities:

```text
train_demo.py
debug_predict.py
```

### `data/samples/`

Contains synthetic sample images used for local testing and demonstration.

### `artifacts/checkpoints/`

Stores locally generated model checkpoints.

The directory is intentionally ignored by Git.

---

# Prerequisites

Before running the project, install the following.

## Python

Python:

```text
3.11+
```

Python 3.12 has been tested during development.

Download:

https://www.python.org/downloads/

On Windows, ensure that Python is added to PATH during installation.

---

## Node.js

Node.js:

```text
18+
```

Node.js 20 is recommended.

Download:

https://nodejs.org/

---

## Git

Git is required for cloning and managing the repository.

Download:

https://git-scm.com/

---

## Disk Space

Approximately 2 GB of free disk space is recommended for Python dependencies and model-related downloads.

---

# Running the Project Locally

The project uses two development processes:

```text
Terminal 1 → FastAPI backend
Terminal 2 → React frontend
```

Start the backend before using the Analyze page.

---

# 1. Clone the Repository

```bash
git clone https://github.com/varshithreddyy6/pneumovision-app.git
cd pneumovision-app
```

---

# 2. Set Up the Backend

Move into the API directory:

```bash
cd services/api
```

Create a virtual environment.

## Windows

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

Your terminal should show:

```text
(.venv)
```

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 3. Install Backend Dependencies

For a CPU-based installation:

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Install the remaining dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# 4. Start the FastAPI Backend

Run:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running.

---

# 5. Train the Demo Model

The repository does not contain a trained checkpoint.

The model checkpoint is intentionally excluded from Git because model files are ignored by `.gitignore`.

From:

```text
services/api
```

with the virtual environment active, run:

```bash
python scripts/train_demo.py
```

The training script creates synthetic demonstration data and a local model checkpoint.

Expected locations:

```text
data/samples/
artifacts/checkpoints/best.pt
```

The demo training pipeline uses DenseNet121 and ImageNet initialization.

Training may take several minutes on CPU.

---

# 6. Verify Model Loading

After training, restart the backend:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/health
```

The model should report as loaded when:

```text
artifacts/checkpoints/best.pt
```

exists and is valid.

Without the checkpoint, the Analyze endpoint can return:

```text
503 Service Unavailable
```

This indicates that the model is unavailable and is expected before the demo model is created.

---

# 7. Start the Frontend

Open a second terminal.

From the repository root:

```bash
cd apps/web
```

Create the local environment file.

## Windows

```powershell
copy .env.example .env
```

## macOS / Linux

```bash
cp .env.example .env
```

For local development, keep:

```env
VITE_API_URL=
```

empty so that the Vite development proxy is used.

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173/
```

---

# 8. Use the Application

Open:

```text
http://localhost:5173/
```

Navigate to the **Analyze** page.

Sample images are available under:

```text
data/samples/
```

Examples:

```text
data/samples/normal_000.png
data/samples/pneumonia_000.png
```

Upload one of the supported images and submit it for analysis.

The interface can display:

* Prediction
* Probability information
* Uncertainty status
* Grad-CAM visualization when available

> ⚠️ Do not upload identity documents, unrelated photographs, screenshots, or sensitive patient information.

---

# API Endpoints

## Health

```http
GET /health
```

Returns service/model health information.

---

## Model

```http
GET /v1/model
```

Returns model/backbone information and loading status.

---

## Analyze

```http
POST /v1/analyze
```

Accepts an uploaded image using a multipart `file` field.

Example:

```bash
curl -X POST \
  http://127.0.0.1:8000/v1/analyze \
  -F "file=@data/samples/pneumonia_000.png"
```

The endpoint validates the upload and performs inference when the model is available.

---

## Metrics

```http
GET /v1/metrics
```

Returns metrics availability information.

The project does not fabricate AUROC or other evaluation values.

---

# Machine Learning Pipeline

The machine-learning workflow can be represented as:

```text
Chest X-Ray
     │
     ▼
Image Validation
     │
     ▼
Preprocessing
     │
     ▼
DenseNet121
     │
     ▼
Binary Classification
     │
     ├──────────────┐
     │              │
     ▼              ▼
  NORMAL       PNEUMONIA
     │              │
     └───────┬──────┘
             ▼
      Probability Score
             │
             ▼
          Grad-CAM
             │
             ▼
     Heatmap / Overlay
```

The primary ML code is located under:

```text
services/api/app/ml/
```

---

# DenseNet121

DenseNet121 is used as the main computer-vision backbone.

The classification workflow produces:

```text
NORMAL
PNEUMONIA
```

The default threshold is:

```text
0.50
```

This is a software configuration setting and is not a medically validated decision boundary.

---

# Grad-CAM Explainability

The project uses Grad-CAM to generate attribution information.

The current target layer is:

```text
features.denseblock4
```

Grad-CAM is useful for understanding which regions influenced the model output.

However, it does not guarantee that highlighted regions correspond to disease.

The visualization can be influenced by:

* Image artifacts
* Devices
* Corner markers
* Background information
* Dataset shortcuts
* Domain shift
* Model limitations

Therefore, Grad-CAM should be treated as model attribution rather than clinical localization.

---

# Configuration

## Frontend

The frontend environment file contains:

```env
VITE_API_URL=
```

Leave this empty when using the local Vite proxy.

---

## Backend

Important configuration values include:

| Configuration        | Purpose                   | Default                         |
| -------------------- | ------------------------- | ------------------------------- |
| `checkpoint_path`    | Model checkpoint location | `artifacts/checkpoints/best.pt` |
| `decision_threshold` | Classification threshold  | `0.50`                          |
| `uncertainty_margin` | Uncertainty band          | `0.10`                          |
| `CORS_ORIGINS`       | Allowed API origins       | Prototype configuration         |

---

# Vite Proxy

During development, Vite proxies API requests to:

```text
127.0.0.1:8000
```

The primary routes include:

```text
/health
/v1
```

This allows the frontend to communicate with the FastAPI backend through the development server.

---

# Testing

## Backend Tests

From:

```text
services/api
```

with the virtual environment active:

```bash
python -m pytest -q
```

---

## Frontend Tests

From:

```text
apps/web
```

run:

```bash
npm test
```

---

## Frontend Production Build

Run:

```bash
npm run build
```

This verifies that the frontend can be compiled for production.

---

# Development and Debugging

## Debug Predictions

From:

```text
services/api
```

run:

```bash
python scripts/debug_predict.py
```

This allows prediction logic to be tested without using the browser.

---

## Backend Troubleshooting

### `No module named uvicorn`

Make sure you are inside:

```text
services/api
```

and that the virtual environment is active:

```text
(.venv)
```

Then run:

```bash
python -m pip install -r requirements.txt
```

Followed by:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Frontend Troubleshooting

### `npm ENOENT package.json`

Make sure you are inside:

```text
apps/web
```

before running:

```bash
npm install
npm run dev
```

---

# Demo Data and Model Files

Synthetic demonstration images are stored under:

```text
data/samples/
```

The local model checkpoint is generated at:

```text
artifacts/checkpoints/best.pt
```

The checkpoint is intentionally not tracked by Git.

The `.gitignore` excludes:

```text
*.pt
*.pth
*.onnx
artifacts/checkpoints/
data/raw/
```

This prevents large model files and raw/clinical data from being accidentally committed.

---

# What Was Worked On

## 1. Product Shell

Built the main product interface with dedicated routes for:

* Home
* Analyze
* Performance
* Explain
* About

A persistent disclaimer and developer information are included as part of the application shell.

---

## 2. API Contract

Implemented a FastAPI service covering:

* Health
* Model information
* Image analysis
* Metrics

The frontend communicates with the backend through an API helper layer.

---

## 3. DenseNet121 Inference

Implemented:

* DenseNet121 integration
* Binary classification
* Model checkpoint loading
* Image preprocessing
* Decision thresholding
* Uncertainty handling
* Inference error handling

---

## 4. Grad-CAM

Implemented Grad-CAM attribution for the DenseNet121 feature hierarchy.

The current attribution target is:

```text
features.denseblock4
```

---

## 5. Demo Training

Implemented a synthetic training workflow that:

* Generates demonstration illustrations
* Uses DenseNet121
* Creates local sample images
* Produces a local model checkpoint
* Allows the complete frontend-to-backend pipeline to be exercised

---

## 6. Validation and Error Handling

The API is designed to handle conditions including:

* Missing upload
* Unsupported file types
* Empty files
* Invalid/corrupted images
* Missing checkpoint
* Inference failures

Grad-CAM failure can be handled separately so that prediction information can still be returned when possible.

---

## 7. Testing

Added:

* Backend tests with pytest
* Frontend tests with Vitest
* Frontend production build validation

---

## 8. Developer Tooling

Implemented:

* Vite development proxy
* Environment templates
* Python virtual-environment workflow
* Demo training script
* Prediction debugging script
* Docker configuration
* Git-friendly project structure

---

# Design and UI

The frontend uses a calm, minimal workstation-inspired visual system.

The documented palette includes:

```text
Paper: #F6F5F2
Ink:   #1A1A1A
```

Typography:

```text
Newsreader
Inter
```

The interface is designed to prioritize:

* Readability
* Clear information hierarchy
* Minimal visual clutter
* Consistent navigation
* Persistent disclaimer visibility

---

# Performance and Evaluation

PneumoVision intentionally avoids presenting fabricated machine-learning performance metrics.

The Performance page remains in an empty state until real evaluation data is available.

A future evaluation pipeline should ideally include:

* Patient-level dataset splitting
* Reproducible train/validation/test partitions
* AUROC
* AUPRC
* Sensitivity
* Specificity
* Precision
* Recall
* F1 score
* Calibration analysis
* Confusion matrix
* Threshold analysis

Demo-model results must not be presented as clinical performance.

---

# Limitations

## Not a Medical Device

PneumoVision has no regulatory clearance and is not intended for clinical use.

---

## Synthetic Demo Model

The included demonstration checkpoint is trained on synthetic illustrations rather than a clinically validated chest X-ray dataset.

The demo model exists to demonstrate the application pipeline.

It does not establish pneumonia-detection performance.

---

## No Clinical Validation

The project does not currently provide:

* Prospective clinical validation
* Hospital validation
* Regulatory evaluation
* Clinical deployment
* Clinically calibrated probabilities

---

## Domain Shift

A model can behave differently when deployed on images that differ from its development data.

Potential differences include:

* Patient population
* Imaging devices
* Image quality
* Positioning
* Acquisition protocols
* Age groups
* Clinical environments
* Dataset composition

---

## Grad-CAM Limitations

Grad-CAM provides model attribution.

It does not prove that an highlighted region represents a pneumonia lesion or clinically meaningful pathology.

---

## Probability Interpretation

Model probabilities should not automatically be interpreted as:

```text
clinical probability
```

or:

```text
diagnostic certainty
```

without proper calibration and clinical validation.

---

# Responsible Use

PneumoVision should be used for:

* Education
* Software development
* Portfolio demonstration
* Machine-learning experimentation
* Research prototyping

It should **not** be used for:

* Diagnosing patients
* Making treatment decisions
* Emergency medical decisions
* Automated patient triage
* Clinical deployment
* Generating medical records
* Autonomous healthcare decisions

Do not upload:

* Patient-identifying information
* Identity documents
* Personal photographs
* Sensitive medical information
* Unrelated images

---

# Docker

The repository includes Docker configuration for **optional / experimental use**:

```text
docker-compose.yml
services/api/Dockerfile
```

Docker support is intended for experimentation and development rather than production deployment.

For the simplest local development workflow, use the Python virtual environment and Node.js setup described above.

---

# Future Improvements

Potential future development includes:

## Real Dataset Training

Replace the synthetic demonstration workflow with a reproducible real-dataset training pipeline.

A future implementation should include metadata such as:

```text
metadata.csv
```

and patient-level grouping to reduce data leakage between training and evaluation sets.

---

## Formal Evaluation

Add a reproducible evaluation pipeline for:

* AUROC
* AUPRC
* Sensitivity
* Specificity
* Precision
* Recall
* F1
* Calibration
* Confusion matrix
* Confidence intervals where appropriate

---

## Model Versioning

Add:

* Model version identifiers
* Training configuration tracking
* Dataset version tracking
* Experiment tracking
* Checkpoint metadata

---

## Improved Explainability

Potential improvements include:

* More robust Grad-CAM handling
* Additional attribution methods
* Improved visualization
* Explanation metadata
* Better image normalization

---

## Production Engineering

Potential future improvements include:

* CI/CD
* Cloud deployment
* Structured logging
* Monitoring
* Authentication
* API rate limiting
* Production-grade CORS configuration
* Better deployment documentation

---

# Git Repository Hygiene

The repository intentionally excludes generated, sensitive, and large files such as:

```text
.venv/
.env
node_modules/
*.pt
*.pth
*.onnx
artifacts/checkpoints/
data/raw/
__pycache__/
.pytest_cache/
.vite/
dist/
```

Environment templates such as:

```text
.env.example
apps/web/.env.example
```

can safely be committed because they contain configuration examples rather than secrets.

Never commit:

* API keys
* Passwords
* Access tokens
* Patient information
* Private credentials
* Large model checkpoints

---

# Contributing

Contributions are welcome for the software and research-development aspects of the project.

Useful contribution areas include:

* Frontend improvements
* Accessibility
* API development
* Test coverage
* ML pipeline improvements
* Explainability improvements
* Documentation
* Developer tooling
* Docker/deployment experimentation

When contributing:

1. Keep the medical disclaimer visible.
2. Do not fabricate performance metrics.
3. Do not claim clinical accuracy without appropriate evidence.
4. Do not commit model weights or sensitive data.
5. Add tests for significant changes.
6. Keep documentation synchronized with the actual implementation.

---

## Recommended Local Checks

Before submitting changes, run the backend tests:

```bash
cd services/api
python -m pytest -q
```

Then run the frontend tests:

```bash
cd ../../apps/web
npm test
```

Finally verify the production build:

```bash
npm run build
```

---

# License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

Any external dataset used with the project remains subject to its own license and usage requirements.

The project does not redistribute clinical datasets.

---

# Author

**Varshith Reddy**

* LinkedIn: [linkedin.com/in/varshithreddyvangeti](https://linkedin.com/in/varshithreddyvangeti)
* GitHub: [github.com/varshithreddyy6](https://github.com/varshithreddyy6)
* Email: [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com)

---

# Repository

https://github.com/varshithreddyy6/pneumovision-app

---

# Final Disclaimer

PneumoVision is an **educational and research software prototype**.

It is not a medical device and is not intended to diagnose, treat, prevent, or make clinical decisions regarding pneumonia or any other medical condition.

The included demo model and synthetic training workflow are intended to demonstrate an end-to-end machine-learning application pipeline.

Model predictions and Grad-CAM visualizations should not be interpreted as clinical diagnoses, clinical probability estimates, or confirmed disease locations.

Any future real-world medical application would require appropriate datasets, rigorous validation, clinical evaluation, safety review, regulatory assessment, and professional oversight.
