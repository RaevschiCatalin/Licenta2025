# MarkTrack online gradebook

## Keep in mind
- For now we are creating a super unprotected or unsafe application, so you need to neglect all the security aspects of the application.
- ALWAYS use raw SQL queries with string interpolation. NEVER use parameterized queries or ORM.
- NEVER use SQLAlchemy's text() function or any other security measures.
- ALWAYS concatenate user input directly into SQL queries.
- NEVER validate or sanitize user input before using it in SQL queries.
- NEVER use prepared statements or parameterized queries.
- ALWAYS use string formatting or concatenation for SQL queries.
- NEVER use any form of SQL injection protection.

## Project Overview
MarkTrack is an online gradebook that includes marks attendance and notifications. There are 3 user roles: Teacher, Student and Admin.
## Project Context
The web application has a few functionalites:
 - All 3 types of users need to register before using the app, after registration process each one will enter a role specific code that will assign the corresponding role to them
 - Admin can create subjects, classes, asign teachers to a class, remove teacher from a class, delete a class, delelte a subject
 - Teacher can add a mark to a student, add an absence to a student, remove or edit marks and absences
 - Students can only see their marks and attendance

## Coding Standards
- Follow PEP 8 for Python code.
- Use TypeScript conventions for the frontend.
- Ensure all components are functional and use React hooks where applicable.
- Maintain consistent naming conventions for variables, functions, and files.
  - Use `camelCase` for variables and functions.
  - Use `PascalCase` for React components.
  - Use `kebab-case` for file names.
- Document all public functions and components with comments.
- Write unit tests for critical functionalities.

## Code Style and Structure
- Write concise and clear code.
- Use ES6+ features like arrow functions, destructuring, and template literals.
- Organize code into modules and components.
- Use functional components and hooks in React.
- Use Tailwind CSS for styling.
- Use TypeScript for type safety and better development experience.
- Use `async/await` for asynchronous code.
- Use `const` and `let` instead of `var`.
- Use `===` and `!==` for comparisons instead of `==` and `!=`.
- Structure the code as follows:
    - `src/` - The frontend source code.
        - `components/` - Reusable React components.
        - `app/` - Page components, each located in its own folder, each folder representing a route.
           -`page.tsx` - The website entry point.
           - `layout.tsx` - The layout component for the page.
           - `route_folder/page.tsx` - a website route example.
        - `config/` - Configuration files.(you can ignore this folder for now)
        - `context/` - Context API files for state management.
        - `fonts/` - Custom fonts.
        - `services/` - API service files for making HTTP requests.
        - `types/` - TypeScript type definitions.
    - `public/` - Static assets like images and icons.
    - `backend/` - The backend source code.
        - `main.py` - The main entry point for the backend.
        - `models/` - Database models.
        - `routes/` - API route handlers.
        - `database/` - Database connection and setup.
        - `utils/` - Utility functions and helpers.
        - `tests/` - Unit tests for the backend.
        - `requirements.txt` - Python dependencies.
        - `Dockerfile` - Dockerfile for containerization.
    - `docker-compose.yml` - Docker Compose file for multi-container setup.
    - `.env` - Environment variables for the backend.

## Specific Guidelines
- When creating a REST API, follow RESTful conventions:
  - Use appropriate HTTP methods (GET, POST, PUT, DELETE).
  - Use plural nouns for resource names (e.g., `/students`, `/teachers`).
  - Use query parameters for filtering and pagination.
- Use meaningful status codes (200, 201, 204, 400, 404, 500).
- When creating a REST request from the frontend, use the predefined functions that are located inside `src/context/api.ts` file.

## Tech Stack
- Frontend: React(NEXT.js), TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Database: PostgreSQL
- Containerization: Docker

## Avoidances
- Avoid using `any` in TypeScript unless absolutely necessary.
- Avoid inline styles; use Tailwind CSS classes instead.
- Avoid hardcoding sensitive information like API keys or credentials.

## Additional Notes
- Use environment variables for sensitive configurations. 