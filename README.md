AI Question & Answering System

A Python question-answering application built using Streamlit and Google’s Gemini AI.

Features

* Interactive chat interface.
* AI-generated answers using Gemini.
* Conversation history during the current session.
* Configurable AI model.
* Error handling and logging.
* Automated tests.

Technologies Used

* Python
* Streamlit
* Google Gemini API
* Pytest

Prerequisites

* Python 3.10 or newer.
* A Google Gemini API key.

Installation

Activate your virtual environment:
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Configuration

Create a .env file from .env.example:
cp .env.example .env

Add your Gemini API key to .env:
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
TEMPERATURE=0.2

Replace the placeholder with your actual API key. Never upload .env to GitHub.

Run the Application
streamlit run app/main.py

Open the local URL shown in the terminal.

Run Tests
pytest

Security

* Never commit .env or expose your API key.
* Keep .env excluded in .gitignore.
* Conversation history is maintained during the active session.

Existing Repository

This application is part of the ai_programs GitHub repository.