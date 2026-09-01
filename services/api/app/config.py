from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "PneumoVision API"
    api_version: str = "0.2.0"
    cors_origins: str = "*"
    checkpoint_path: str = "artifacts/checkpoints/best.pt"
    image_size: int = 224
    decision_threshold: float = 0.50
    uncertainty_margin: float = 0.10

    @property
    def origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


settings = Settings()

DISCLAIMER = (
    "This application is an educational/research screening prototype. "
    "It is not a medical device and must not be used to diagnose, treat, "
    "or make clinical decisions. Results require qualified professional interpretation."
)
