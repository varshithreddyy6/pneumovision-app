from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import state
from app.config import DISCLAIMER, settings
from app.ml.engine import InferenceEngine
from app.routers import analyze, health, metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.engine = InferenceEngine.try_load()
    yield
    state.engine = None


app = FastAPI(
    title="PneumoVision API",
    version=settings.api_version,
    lifespan=lifespan,
    description="Educational pneumonia screening prototype. " + DISCLAIMER,
)

_origins = ["*"] if settings.cors_origins.strip() == "*" else settings.origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, (HTTPException, RequestValidationError)):
        raise exc
    return JSONResponse(
        status_code=500,
        content={
            "detail": {
                "code": "unhandled",
                "message": f"{type(exc).__name__}: {exc}",
                "disclaimer": DISCLAIMER,
            }
        },
    )


app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(metrics.router)


@app.get("/")
def root() -> dict:
    return {
        "service": settings.app_name,
        "docs": "/docs",
        "health": "/health",
        "disclaimer": DISCLAIMER,
        "model_loaded": state.engine is not None,
    }
