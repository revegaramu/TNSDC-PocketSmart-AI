# POCKETSMART AI

## AI-Powered Budget-Based Recommendation System

### Project Documentation

---

# 1. Cover Page

**Project Title:** PocketSmart AI

**Project Type:** GenAI-Powered Recommendation System

**Technology:** Python, FastAPI, Jinja2, Google Gemini

**Submitted By:**  
Team Members: ______________________

**Institution:** ______________________

**Academic Year:** 2026

---

# 2. Certificate

This is to certify that the project titled **“PocketSmart AI”** has been developed as part of the academic/project requirements.

---

# 3. Declaration

We hereby declare that the project titled **“PocketSmart AI”** is our project work and has been developed for educational purposes.

---

# 4. Acknowledgement

We express our sincere gratitude to our faculty members, mentors, institution, and project coordinators for their guidance and support throughout the development of this project.

---

# 5. Abstract

PocketSmart AI is an AI-powered recommendation system designed to help users make budget-conscious decisions for different planning needs.

The system provides recommendations based on user preferences, requirements, and budget constraints. The application includes planning features for home-related requirements, party planning, and jewelry-related recommendations.

The system is developed using Python and FastAPI for the backend, Jinja2 for the web interface, and Google Gemini integration for AI-powered recommendations. A fallback recommendation mechanism is also included so that the application can continue providing recommendations when the AI service is unavailable.

---

# 6. Introduction

In today's digital environment, users often have to compare a large number of products and services before making purchasing or planning decisions.

PocketSmart AI addresses this problem by providing a centralized recommendation platform that considers the user's requirements and budget.

The project aims to simplify decision-making by generating relevant recommendations through an AI-assisted system.

---

# 7. Problem Statement

Users may find it difficult to select suitable products and services because of:

- Large numbers of available choices
- Different price ranges
- Limited time for comparison
- Difficulty staying within a budget
- Lack of personalized recommendations

PocketSmart AI attempts to address these challenges through an intelligent recommendation platform.

---

# 8. Existing System

Traditional recommendation and planning methods may require users to manually search different websites and compare products.

Common limitations include:

- Manual comparison
- Time-consuming searches
- Generic recommendations
- Difficulty managing budgets
- Information scattered across different platforms

---

# 9. Proposed System

PocketSmart AI provides a centralized web application where users can enter their requirements and receive recommendations.

The proposed system includes:

- User registration
- User login
- Dashboard
- Home planning
- Party planning
- Jewelry assistance
- Budget-based recommendations
- AI-assisted recommendation generation
- Recommendation history

---

# 10. Objectives

The major objectives of PocketSmart AI are:

1. To provide personalized recommendations.
2. To consider user budget constraints.
3. To simplify planning and decision-making.
4. To provide multiple planning modules.
5. To integrate Generative AI.
6. To provide a simple web interface.
7. To maintain recommendation history.

---

# 11. Scope

The system can be used for:

- Home planning
- Party planning
- Jewelry-related assistance
- Budget-based recommendations
- Personalized planning

The system can be further extended to additional product and service categories.

---

# 12. Project Description

PocketSmart AI is a web-based AI recommendation application.

Users can create an account and access the dashboard. From the dashboard, they can select different planning modules and enter their requirements.

The recommendation service processes the input and generates suitable recommendations.

---

# 13. Functional Requirements

The system provides the following functional requirements:

- User registration
- User authentication
- User login
- User logout
- Dashboard access
- Home planning
- Party planning
- Jewelry assistance
- Recommendation generation
- Recommendation history
- Image upload for the jewelry module

---

# 14. Non-Functional Requirements

The system should provide:

- Usability
- Reliability
- Security
- Maintainability
- Performance
- Scalability

---

# 15. System Architecture

The main architecture consists of:

1. User Interface
2. FastAPI Application
3. Authentication Layer
4. Recommendation Service
5. Database Layer
6. Google Gemini AI Service

---

# 16. System Workflow

The basic workflow is:

User
↓
Registration/Login
↓
Dashboard
↓
Select Planning Module
↓
Enter Requirements
↓
Recommendation Service
↓
AI Recommendation / Fallback Recommendation
↓
Display Results
↓
Save Recommendation History

---

# 17. Data Flow

The user enters requirements through the web interface.

The FastAPI backend receives the request and validates the input.

The recommendation service processes the information and generates recommendations.

The resulting recommendations are displayed to the user.

---

# 18. Database Design

PocketSmart AI uses a database to store application information such as:

- User information
- Authentication-related information
- Planning requests
- Recommendation history

The project includes the database file:

`pocketsmart.db`

---

# 19. Technology Stack

## Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates

## Backend

- Python
- FastAPI
- Uvicorn

## AI

- Google Gemini API

## Database

- SQLite

## Testing

- Pytest

## Development Environment

- Visual Studio Code
- Git
- GitHub

---

# 20. Module Description

## 20.1 Authentication Module

Handles user registration, login, logout, and session management.

## 20.2 Dashboard Module

Provides access to the different planning features.

## 20.3 Home Planner

Provides recommendations related to home requirements based on user inputs and budget.

## 20.4 Party Planner

Provides recommendations for party-related planning.

## 20.5 Jewelry Assistant

Provides jewelry-related recommendations based on user preferences and inputs.

## 20.6 Recommendation Service

Processes user requirements and generates recommendations using the AI service or fallback recommendation mechanism.

## 20.7 History Module

Stores and displays previous recommendation results.

---

# 21. User Interface Design

The application provides a web-based interface that allows users to interact with the recommendation system.

The major pages include:

- Home Page
- Login Page
- Registration Page
- Dashboard
- Home Planner
- Party Planner
- Jewelry Assistant
- Recommendation Results
- History

---

# 22. Home Page

The home page introduces PocketSmart AI and provides navigation to the application.

[Insert Home Page Screenshot Here]

---

# 23. Login and Registration

Users can create an account and log into the system.

[Insert Login Screenshot Here]

[Insert Registration Screenshot Here]

---

# 24. Dashboard

The dashboard provides access to the different planning modules.

[Insert Dashboard Screenshot Here]

---

# 25. Home Planner

The Home Planner accepts user requirements and budget information and generates suitable recommendations.

[Insert Home Planner Screenshot Here]

---

# 26. Party Planner

The Party Planner helps users organize party-related requirements based on their inputs.

[Insert Party Planner Screenshot Here]

---

# 27. Jewelry Assistant

The Jewelry Assistant provides jewelry-related recommendations based on user requirements.

[Insert Jewelry Assistant Screenshot Here]

---

# 28. AI Recommendation Process

The recommendation process follows these steps:

1. User enters requirements.
2. Backend validates the request.
3. Recommendation service processes the input.
4. Gemini AI is used when configured and available.
5. The fallback recommendation system is used when necessary.
6. Results are returned to the user.
7. Recommendation history can be stored.

---

# 29. Project Development

The project was developed using a modular architecture.

The main application components include:

- FastAPI application
- Configuration
- Database
- Authentication
- Recommendation services
- HTML templates
- Static CSS and JavaScript
- Automated tests

---

# 30. Testing

Testing was performed using Pytest.

The application was tested to verify that the configured application functionality works correctly.

---

# 31. Test Results

The Phase 6 automated test produced the following result:

**Tests Passed:** 1

**Tests Failed:** 0

**Warnings:** 3

**Execution Time:** Approximately 0.18 seconds

**Overall Result:** PASS

The warnings were related to a FastAPI `on_event` deprecation notice and did not cause the test to fail.

---

# 32. Advantages

- Budget-conscious recommendations
- AI-assisted decision support
- Multiple planning modules
- Simple web interface
- User authentication
- Recommendation history
- Fallback recommendation mechanism

---

# 33. Limitations

- Recommendation quality depends on the available input information.
- AI-based recommendations may require API access.
- External product availability and prices may change.
- The current system can be expanded with additional recommendation categories.

---

# 34. Future Enhancements

Future versions could include:

- More planning categories
- Real-time product prices
- E-commerce integration
- Advanced image analysis
- Improved personalization
- Mobile application
- Voice-based interaction
- Advanced analytics
- More sophisticated recommendation models

---

# 35. Conclusion

PocketSmart AI demonstrates how Generative AI can be integrated into a practical recommendation system.

The project provides a centralized platform for budget-based planning and recommendations across multiple categories.

The system combines a FastAPI backend, web interface, database, authentication, recommendation services, and AI integration.

The successful automated test demonstrates that the currently configured application functionality can be tested through the project's testing framework.

---

# 36. References

1. FastAPI Documentation
2. Python Documentation
3. Pytest Documentation
4. Google Gemini Documentation
5. Jinja2 Documentation
6. SQLite Documentation
7. Git Documentation
8. GitHub Documentation