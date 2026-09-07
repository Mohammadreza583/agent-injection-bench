"""Environment-backed configuration for the agent harness."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    base_url: str
    model: str

    @property
    def configured(self) -> bool:
        return bool(self.api_key.strip())


def load_config(*, dotenv_path: str | None = None) -> LLMConfig:
    """Load LLM settings from environment (.env optional)."""
    load_dotenv(dotenv_path=dotenv_path, override=False)
    api_key = (
        os.getenv("AIB_LLM_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    )
    base_url = os.getenv("AIB_LLM_BASE_URL", "https://api.openai.com/v1").strip()
    model = os.getenv("AIB_LLM_MODEL", "gpt-4o-mini").strip()
    return LLMConfig(api_key=api_key, base_url=base_url, model=model)
