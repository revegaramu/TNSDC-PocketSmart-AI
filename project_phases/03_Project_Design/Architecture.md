# PocketSmart AI – System Architecture

PocketSmart AI follows a client-server architecture.

## Frontend

The frontend provides the user interface.

Technologies:

- HTML
- CSS
- JavaScript
- Jinja2 templates

## Backend

The backend is developed using FastAPI.

Responsibilities:

- Authentication
- Request validation
- Recommendation processing
- Database interaction
- API endpoints

## Database

SQLite is used for storing:

- User accounts
- Recommendation history

## AI Layer

Google Gemini can be used to generate personalized recommendations.

A local fallback recommendation engine is also provided.

## Architecture Flow

User
 ↓
Frontend
 ↓
FastAPI Backend
 ↓
Recommendation Service
 ↓
Gemini AI / Local Recommendation Engine
 ↓
SQLite Database
 ↓
Result displayed to User