# PocketSmart AI

PocketSmart AI is a budgeting and recommendation application built with
FastAPI, SQLite, HTML, CSS, JavaScript, and optional Google Gemini AI.

## Features

- User registration and login
- Secure password hashing
- Session-based authentication
- Home planning recommendations
- Party planning recommendations
- Jewelry suggestions
- Optional outfit image upload
- Saved recommendation history
- Optional Gemini AI integration
- Local recommendation fallback
- REST API and Swagger documentation

## Requirements

- Python 3.11 or newer
- Visual Studio Code
- Internet connection for installing packages
- Optional Gemini API key

## Setup on Windows

Open the project folder in VS Code.

Create a virtual environment:

    py -m venv .venv

Activate it in PowerShell:

    .venv\Scripts\Activate.ps1

If PowerShell blocks activation, use Command Prompt:

    .venv\Scripts\activate.bat

Install dependencies:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

Create the environment file:

    Copy-Item .env.example .env

Edit `.env` and replace the example secret key.

Start the application:

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000

API documentation:

    http://127.0.0.1:8000/docs

Health check:

    http://127.0.0.1:8000/health

## Enable Gemini

Add your API key to `.env`:

    GEMINI_API_KEY=your_actual_api_key
    GEMINI_MODEL=gemini-2.5-flash

Restart the server after changing environment variables.

Without a key, the application uses its local recommendation engine.

## Run tests

    python -m pytest -q

## Database

SQLite creates `pocketsmart.db` in the project directory by default.

The database contains:

- users
- recommendations

## API endpoints

- GET /health
- GET /startup
- POST /register
- POST /login
- POST /logout
- GET /dashboard
- GET /session-info
- GET /session-data
- POST /token
- POST /generate-home
- POST /generate-party
- POST /generate-jewelry
- POST /generate-jewelry-with-image
- POST /recommendations-details
- GET /history
- GET /result/{recommendation_id}

## Notes

- Prices are estimates, not live quotations.
- Product availability is not checked.
- The image upload endpoint accepts images but does not currently
  analyze their visual contents.
- Browser authentication uses signed session cookies.
- The `/token` endpoint is a compatibility endpoint, not a JWT issuer.

## Production checklist

Before deploying publicly:

- Set a strong, unique SECRET_KEY.
- Enable HTTPS and SESSION_HTTPS_ONLY.
- Add CSRF protection to browser form submissions.
- Add login and registration rate limits.
- Add email verification and account recovery.
- Configure database backups.
- Review privacy and image-upload retention policies.
- Add monitoring and structured logging.
- Validate all AI-generated output before displaying it.