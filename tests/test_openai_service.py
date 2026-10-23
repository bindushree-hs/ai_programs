"""Tests for the OpenAI service without network access."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from openai import APIError

from app.config.settings import Settings
from app.services.openai_service import OpenAIService, OpenAIServiceError


@pytest.fixture
def settings() -> Settings:
    return Settings(
        openai_api_key="test-key",
        openai_model="gpt-test",
        temperature=0.2,
    )


@patch("app.services.openai_service.OpenAI")
def test_initializes_client_with_configured_key(
    openai_constructor: Mock, settings: Settings
) -> None:
    service = OpenAIService(settings)

    openai_constructor.assert_called_once_with(api_key="test-key")
    assert service is not None


@patch("app.services.openai_service.OpenAI")
def test_returns_response_text_and_sends_conversation(
    openai_constructor: Mock, settings: Settings
) -> None:
    client = openai_constructor.return_value
    client.responses.create.return_value = SimpleNamespace(
        output_text="  A clear answer.  "
    )
    service = OpenAIService(settings)
    messages = [
        {"role": "user", "content": "First question"},
        {"role": "assistant", "content": "First answer"},
        {"role": "user", "content": "Follow-up"},
    ]

    answer = service.generate_answer(messages)

    assert answer == "A clear answer."
    request = client.responses.create.call_args.kwargs
    assert request["model"] == "gpt-test"
    assert request["temperature"] == 0.2
    assert request["input"][1:] == messages
    assert request["input"][0]["role"] == "system"


@patch("app.services.openai_service.OpenAI")
def test_omits_temperature_when_not_supported(
    openai_constructor: Mock,
) -> None:
    client = openai_constructor.return_value
    client.responses.create.return_value = SimpleNamespace(output_text="Answer")
    settings = Settings(openai_api_key="test-key", openai_model="gpt-5-mini")
    service = OpenAIService(settings)

    assert service.generate_answer([{"role": "user", "content": "question"}]) == "Answer"
    assert "temperature" not in client.responses.create.call_args.kwargs


@patch("app.services.openai_service.OpenAI")
def test_does_not_expose_openai_error_details(
    openai_constructor: Mock, settings: Settings
) -> None:
    client = openai_constructor.return_value
    client.responses.create.side_effect = APIError(
        "sensitive diagnostic text",
        request=Mock(),
        body=None,
    )
    service = OpenAIService(settings)

    with pytest.raises(OpenAIServiceError, match="temporarily unavailable") as error:
        service.generate_answer([{"role": "user", "content": "question"}])

    assert "sensitive diagnostic text" not in str(error.value)
