# R Fitness

A gym website and lead-management dashboard for R Fitness, Uppal, Hyderabad.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Bootstrap 5
- API: FastAPI, Pydantic, SQLAlchemy 2, Alembic
- Database: Neon PostgreSQL
- Admin authentication: app-managed email/password login, Argon2 password hashing in memory, signed JWTs
- Hosting: one Render Docker web service serving both FastAPI and the built Vue site

## Repository layout

```text
frontend/       Vue website and admin dashboard
backend/        FastAPI application, migrations and Dockerfile
render.yaml     Single Docker service Blueprint
```

## Local development

### Backend

Python 3.12+ is recommended.

```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env
```

Set `DATABASE_URL` to the Neon PostgreSQL connection string. Use the pooled connection string and keep `sslmode=require` enabled. The app adapts standard `postgresql://` URLs to psycopg.

Configure `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and a random `JWT_SECRET` of at least 32 characters in `backend/.env`. The API hashes the configured password with Argon2 in process memory; it does not store a password hash in the database or require a hash environment variable.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  
Health check: http://localhost:8000/healthz

### Frontend development

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173. Vite calls the local API at http://localhost:8000. In production, leave `VITE_API_BASE_URL` unset: the Vue site and API are served from the same origin by one Docker service.

## Neon database setup

1. Create a Neon project and database.
2. Copy the pooled connection string from the Neon dashboard. Keep `sslmode=require` enabled.
3. Set the string as `DATABASE_URL` on the Render Docker service (or in local `backend/.env`).
4. Alembic migrations are applied automatically by the Docker entrypoint before FastAPI starts.

The browser never connects directly to PostgreSQL. All application data goes through FastAPI.

## Admin authentication

- Login endpoint: `POST /api/v1/auth/login`.
- `ADMIN_EMAIL` controls the admin login email.
- `ADMIN_PASSWORD` contains the password as a Render runtime secret.
- The API derives an Argon2 password hash in process memory when the password is first used. The hash is not saved to Neon or written to disk.
- `JWT_SECRET` signs access tokens. Render generates this value automatically for the deployed service and keeps it stable across deploys.
- Tokens expire after eight hours. The dashboard keeps the token in the current browser tab's session storage.
- All admin API routes validate the signed token server-side.

Render also generates a strong random `ADMIN_PASSWORD` automatically. Find it in the service's Environment page in the Render Dashboard. The default admin email is `admin@rfitness.local`; you can change it through `ADMIN_EMAIL`.

## Render deployment

The root `render.yaml` creates one Docker web service named `r-fitness`. The multi-stage Docker build:
1. Builds the Vue app using Node.
2. Installs FastAPI runtime dependencies using Python.
3. Copies the built Vue assets into the Python image.
4. Runs Alembic migrations and starts Uvicorn.

Only one manually supplied environment variable is required:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL pooled connection string |

Render generates `ADMIN_PASSWORD` and `JWT_SECRET`; `ADMIN_EMAIL` and `APP_ENV` have defaults in `render.yaml`. The container serves the website, admin dashboard and API from one origin, so no frontend API URL or production CORS setting is required.

## Before publishing

The initial content uses the public business listing for the gym's name, address and phone. Confirm these with the owner before launch. Membership prices, exact services, trainer profiles, class schedules and Sunday hours are intentionally not invented; populate them after the owner confirms the details. Replace representative stock photos with original R Fitness photographs before publishing.

## MVP included

- Responsive public gym website
- Membership plans (no invented prices)
- Trial / membership enquiry form stored in Neon PostgreSQL
- App-managed administrator login with Argon2 and JWT
- Admin enquiry inbox with status updates
- Admin membership-plan management
- Single multi-stage Docker image for website + API
- Database migrations, health check and Render Blueprint

Member accounts, payments, attendance, trainer management UI and class booking are future phases.
