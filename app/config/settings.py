"""Environment-backed application settings."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
class ConfigurationError(ValueError):
    """Raised when required application configuration is unavailable."""
@dataclass(frozen=True)
class Settings:
    """Settings required to configure the Gemini service."""
    gemini_api_key: str
    gemini_model: str = "gemini-3.5-flash"
    temperature: float = 0.2
    @classmethod
    def from_env(cls) -> "Settings":
        """Load and validate settings from environment variables."""
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ConfigurationError(
                "GEMINI_API_KEY is missing. Add your Gemini API key to the .env file."
            )
        model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
        if not model:
            raise ConfigurationError("GEMINI_MODEL must not be empty.")
        raw_temperature = os.getenv("TEMPERATURE", "0.2").strip()
        try:
            temperature = float(raw_temperature)
        except ValueError as exc:
            raise ConfigurationError(
                "TEMPERATURE must be a number between 0 and 2."
            ) from exc
        if not 0 <= temperature <= 2:
            raise ConfigurationError("TEMPERATURE must be between 0 and 2.")
        return cls(
            gemini_api_key=api_key,
            gemini_model=model,
            temperature=temperature,
        )