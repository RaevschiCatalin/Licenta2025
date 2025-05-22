# MarkTrack Secured Implementation Rules

## Keep in Mind
This phase focuses on **maximum security**. You must address and mitigate all previously introduced vulnerabilities.

---

## 🔐 Security Practices

### Password Handling
- ALWAYS hash passwords using a secure hashing algorithm (e.g., `bcrypt`) before storing them.
- NEVER store or transmit plaintext passwords.
- NEVER return password hashes in API responses.

### SQL & Database
- ALWAYS use parameterized queries or ORM (e.g., SQLAlchemy ORM or SQLModel).
- NEVER use string interpolation or manual SQL query building.
- VALIDATE all user input before using it in queries.
- SANITIZE input that may be rendered to prevent XSS.

### Input Validation
- STRICTLY validate and sanitize all user inputs using `pydantic` models.
- LIMIT field lengths and disallow invalid characters.

### Authentication
- USE secure JWT-based authentication.
- SECURE all endpoints based on roles: Admin, Teacher, Student.
- USE HTTP-only and secure cookies or authorization headers to store tokens.

### Access Control
- IMPLEMENT Role-Based Access Control (RBAC).
- NEVER allow unauthorized users to access protected resources or perform restricted operations.

### Transport Security
- ONLY serve the app over HTTPS in production.
- NEVER expose sensitive environment variables or Docker secrets publicly.

### Frontend Security
- ENABLE CSRF protection on all state-changing requests (if using cookies).
- SANITIZE all user-generated content before rendering.
- DO NOT leak tokens, secrets, or internal data to the frontend.

### Error Handling
- NEVER expose full stack traces or error internals to users.
- RETURN generic error messages with correct HTTP status codes.

### Secrets Management
- NEVER hardcode secrets or credentials in code.
- ALWAYS use environment variables (`.env`) and Docker secrets.

### Testing
- WRITE unit and integration tests for:
  - Authentication
  - Authorization
  - Input validation
  - Critical data modification endpoints

---

## Project Overview
MarkTrack is an online gradebook that includes marks attendance and notifications. There are 3 user roles: Teacher, Student and Admin.

## Project Context
The web application has a few functionalities:
- All 3 types of users need to register before using the app, after registration process each one will enter a role specific code that will assign the corresponding role to them
- Admin can create subjects, classes, assign teachers to a class, remove teacher from a class, delete a class, delete a subject
- Teacher can add a mark to a student, add an absence to a student, remove or edit marks and absences
- Students can only see their marks and attendance

## Project Hygiene

- Use PEP8 for Python and clean TS/JS for frontend.
- Consistent naming: `camelCase` for variables, `PascalCase` for components.
- Follow RESTful conventions and correct HTTP status codes.
- Secure database credentials and JWT secrets using `.env`.
- Write concise and clear code.
- Use ES6+ features like arrow functions, destructuring, and template literals.
- Use functional components and hooks in React.
- Use Tailwind CSS for styling.
- Use TypeScript for type safety and better development experience.
- Use `async/await` for asynchronous code.
- Use `const` and `let` instead of `var`.
- Use `===` and `!==` for comparisons instead of `==` and `!=`.

## Project Structure
- `src/` - The frontend source code.
    - `components/` - Reusable React components.
    - `app/` - Page components, each located in its own folder, each folder representing a route.
       - `page.tsx` - The website entry point.
       - `layout.tsx` - The layout component for the page.
       - `route_folder/page.tsx` - a website route example.
    - `config/` - Configuration files.
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

## Branch & Data Strategy

- `main` branch will be used for the secure version.
- `vulnerable` branch is preserved for security testing.
- Use **separate Postgres databases**:
  - `vulnerable_db` for the insecure app.
  - `marktrack_db` for the secure version.

## Tech Stack
- Frontend: React(NEXT.js), TypeScript, Tailwind CSS
- Backend: Python, FastAPI
- Database: PostgreSQL
- Containerization: Docker

## Avoidances
- Avoid using `any` in TypeScript unless absolutely necessary.
- Avoid inline styles; use Tailwind CSS classes instead.
- Avoid hardcoding sensitive information like API keys or credentials.
