"""Streamlit user interface for the question-answering application."""

import logging

import streamlit as st

from app.config.settings import ConfigurationError, Settings
from app.services.openai_service import OpenAIService, OpenAIServiceError
from app.utils.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def _get_service(settings: Settings) -> OpenAIService:
    """Create a service using the current application settings."""
    return OpenAIService(settings)

def _render_history() -> None:
    """Render the existing conversation."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    """Render the application and handle submitted questions."""
    st.set_page_config(
        page_title="AI Question & Answering System",
        page_icon="💬",
    )

    st.title("AI Question & Answering System")
    st.write(
        "Ask a question and get a response powered by Google Gemini."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        st.error(str(exc))
        st.stop()

    with st.sidebar:
        st.subheader("About this session")
        st.write(f"**Model:** `{settings.gemini_model}`")
        st.write(f"**Temperature:** `{settings.temperature:g}`")

        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    _render_history()

    question = st.chat_input("Type your question here...")

    if question is None:
        return

    question = question.strip()

    if not question:
        st.warning("Please enter a question before submitting.")
        return

    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(question)

    try:
        service = _get_service(settings)

        with st.chat_message("assistant"):
            status = st.status(
                "Connecting to Gemini...",
                expanded=True,
            )

            try:
                status.write("Sending your question to the AI model...")
                answer = service.generate_answer(
                    st.session_state.messages
                )

                if not answer or not answer.strip():
                    raise OpenAIServiceError(
                        "Gemini returned an empty answer. Please try again."
                    )

                status.update(
                    label="Answer generated successfully!",
                    state="complete",
                    expanded=False,
                )

                st.markdown(answer)

            except OpenAIServiceError as exc:
                status.update(
                    label="Could not generate an answer",
                    state="error",
                    expanded=True,
                )
                st.error(str(exc))
                logger.warning("Gemini service error: %s", exc)
                return

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
        logger.info("Successfully generated an answer.")

    except Exception as exc:
        logger.exception("Unexpected application error.")
        st.error(
            "Something went wrong in the application. "
            "Check the VS Code terminal for the error details."
        )


if __name__ == "__main__":
    main()