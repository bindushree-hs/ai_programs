"""Google Gemini integration for the Question & Answering application."""

import time
import logging

from google import genai

from google.genai import errors, types

from app.config.settings import Settings

logger = logging.getLogger(__name__)

class OpenAIServiceError(RuntimeError):

    """Raised when an answer cannot be generated."""

class OpenAIService:

    """Generate answers using Google Gemini."""

    def __init__(self, settings: Settings) -> None:

        self._settings = settings

        self._client = genai.Client(

            api_key=settings.gemini_api_key,

            http_options=types.HttpOptions(

                timeout=30000,

                retry_options=types.HttpRetryOptions(attempts=1),

            ),

        )

    def generate_answer(self, messages: list[dict[str, str]]) -> str:

        """Generate an answer using the conversation history."""

        if not messages:

            raise ValueError("Please enter a question.")

        conversation = []

        for message in messages:

            content = message.get("content", "").strip()

            if not content:

                continue

            role = message.get("role", "user")

            label = "Assistant" if role == "assistant" else "User"

            conversation.append(f"{label}: {content}")

        if not conversation:

            raise ValueError("Please enter a question.")

        prompt = (

            "You are a helpful question-answering assistant. "

            "Give clear, accurate, easy-to-understand answers.\n\n"

            + "\n\n".join(conversation)

        )

        try:

            start_time = time.time()

            logger.info(
                 "Sending request to Gemini model: %s",
                 self._settings.gemini_model,
            )

        

            response = self._client.models.generate_content(

                model=self._settings.gemini_model,

                contents=prompt,

                config=types.GenerateContentConfig(

                    temperature=self._settings.temperature,

                ),

            )

            answer = response.text

            if not answer or not answer.strip():

                raise OpenAIServiceError(

                    "Gemini returned an empty answer. Please try another question."

                )

            logger.info(
                "Gemini successfully generated an answer in %.2f seconds.",
                time.time() - start_time,
            )

            return answer.strip()

        except OpenAIServiceError:

            raise

        except errors.APIError as exc:
            logger.error(
                "Gemini API error: code=%s, message=%s",
                getattr(exc, "code", "unknown"),
                str(exc),
            )

            if getattr(exc, "code", None) in (429, 500, 502, 503, 504):
                raise OpenAIServiceError(
                    "Gemini is temporarily busy or unavailable. "
                    "Please submit your question again in a few seconds."
                ) from None

            raise OpenAIServiceError(
               f"Gemini could not complete the request: {exc}"
            ) from None

        except Exception as exc:

            logger.exception("Unexpected Gemini error.")

            raise OpenAIServiceError(

                f"An unexpected error occurred: {type(exc).__name__}. "

                "Please check the terminal for details."

            ) from None