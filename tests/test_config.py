"""Tests for environment-backed configuration."""

import pytest

from app.config.settings import ConfigurationError, Settings


def test_loads_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("TEMPERATURE", "0.7")

    settings = Settings.from_env()

    assert settings.openai_api_key == "test-key"
    assert settings.openai_model == "gpt-test"
    assert settings.temperature == 0.7


def test_gpt5_model_does_not_load_unsupported_temperature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-5-mini")
    monkeypatch.setenv("TEMPERATURE", "0.2")

    settings = Settings.from_env()

    assert settings.openai_model == "gpt-5-mini"
    assert settings.temperature is None


def test_missing_api_key_has_configuration_guidance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ConfigurationError, match=r"Create a \.env file"):
        Settings.from_env()


@pytest.mark.parametrize("temperature", ["not-a-number", "-0.1", "2.1"])
def test_rejects_invalid_temperature(
    monkeypatch: pytest.MonkeyPatch, temperature: str
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("TEMPERATURE", temperature)

    with pytest.raises(ConfigurationError):
        Settings.from_env()
