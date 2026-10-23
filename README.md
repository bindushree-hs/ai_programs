# AI Question & Answering System

A Streamlit chat application that answers questions with OpenAI's GPT-5 mini model by default. It keeps conversation history for the active Streamlit session, so follow-up questions can use earlier context.

## Features

- Chat-style question and answer interface with streamed-session history.
- Configurable model, with temperature sent only to models that support it.
- Loading indicator, conversation reset, and friendly errors.
- Validates configuration and questions before requesting an answer.
- Unit tests use a mocked OpenAI client and make no network calls.

## Architecture

The Streamlit UI is in `app/main.py`. Environment configuration and validation live in `app/config/settings.py`; the OpenAI Responses API integration is encapsulated in `app/services/openai_service.py`; system instructions are maintained in `app/prompts/qa_prompt.py`; and standard logging is configured in `app/utils/logging_config.py`.

## Project structure

```text
question_answering_app/
├── app/
│   ├── config/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.sh
```

## Prerequisites

- Python 3.10 or newer.
- An OpenAI API key with access to the configured model.
- `pip`.

## Setup

Run these commands from the `question_answering_app` project directory.

### Create and activate a virtual environment

```sh
python -m venv .venv
```

macOS/Linux:

```sh
source .venv/bin/activate
```

Windows Command Prompt:

```bat
.venv\Scripts\activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Configure the API key

Copy `.env.example` to `.env`, then replace the placeholder with your API key:

macOS/Linux:

```sh
cp .env.example .env
```

Windows Command Prompt:

```bat
copy .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Set the following values in `.env`:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5-mini
```

`OPENAI_API_KEY` is required. `OPENAI_MODEL` defaults to `gpt-5-mini`. GPT-5 models do not use the `TEMPERATURE` setting; it is omitted from their API requests. For other models that support temperature, `TEMPERATURE` defaults to `0.2` and must be between 0 and 2.

## Run the application

From the project directory, with the virtual environment activated:

```sh
streamlit run app/main.py
```

Alternatively, on macOS/Linux, use `./run.sh`. Streamlit prints the local URL in the terminal. Use **Clear Conversation** in the sidebar to start over.

## Run tests

```sh
pytest
```

Tests mock the OpenAI SDK, so they do not need a real API key and do not make API requests.

## Example questions

- “Explain how photosynthesis works in a few steps.”
- “What are the trade-offs between SQL and NoSQL databases?”
- “Can you summarize that answer in one paragraph?” (follow-up)

## Troubleshooting

- **Missing API key:** Create `.env` from `.env.example`, then set `OPENAI_API_KEY`.
- **Authentication or API error:** Check that the key is valid and has access to the configured model. The UI intentionally does not show sensitive SDK diagnostics.
- **Model errors:** Verify the model name and that your API key has access to it. Temperature is only sent to models that support it.
- **Command not found:** Activate `.venv` and install dependencies with `pip install -r requirements.txt`.
- **Port already in use:** Start Streamlit on another port, for example `streamlit run app/main.py --server.port 8502`.

## Security considerations

- Never commit `.env` or share the API key. `.env` is ignored by Git.
- `.env.example` contains placeholders only.
- The application does not display or log the API key, and does not log conversation content.
- Use a restricted API key, rotate it if exposed, and configure deployment secrets through the hosting platform rather than committing secrets.
- Conversation history is held in Streamlit session state and is not persisted by this application.

## Stop the application and deactivate the environment

Stop the Streamlit server with `Ctrl+C` in the terminal where it is running. Deactivate the virtual environment with:

```sh
deactivate
```

## Future enhancements

- Add optional conversation export and configurable history limits.
- Add deployment health checks, metrics, and rate limiting.
- Add broader integration tests against a controlled mock HTTP transport.
- Add accessibility and browser-based UI tests.
