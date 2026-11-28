# R Fitness

A gym website and lead-management dashboard for R Fitness, Uppal, Hyderabad.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Bootstrap 5
- API: FastAPI, Pydantic, SQLAlchemy 2, Alembic
- Database: Neon PostgreSQL
- Admin authentication: one-time generated password, Argon2 hash and persisted JWT signing key
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

Set only `DATABASE_URL` in `backend/.env` to your Neon PostgreSQL connection string. Keep `sslmode=require` enabled.

```bash
alembic upgrade head
python -m app.bootstrap_admin
uvicorn app.main:app --reload
```

The first bootstrap prints a randomly generated administrator password once. Use email `admin@rfitness.local` and that generated password to sign in at `/admin`. The password hash and JWT signing key are stored in Neon; the plaintext password is not stored.

### Frontend development

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173. Vite calls the local API at http://localhost:8000. In production, the Vue site and API are served from the same origin by one Docker service.

## Neon database setup

1. Create a Neon project and database.
2. Copy the pooled connection string from the Neon dashboard. Keep `sslmode=require` enabled.
3. Set it as `DATABASE_URL` on Render (or in local `backend/.env`).
4. Alembic migrations and the one-time administrator bootstrap run automatically when the Docker container starts.

The browser never connects directly to PostgreSQL. All application data goes through FastAPI.

## Admin authentication

- Login endpoint: `POST /api/v1/auth/login`.
- The default administrator email is `admin@rfitness.local`.
- On first boot, the app generates a cryptographically random admin password and a separate JWT signing secret.
- The password is Argon2-hashed and stored in the Neon `app_admin_credentials` table. The JWT signing secret is persisted in the same private table so sessions remain valid across restarts.
- The plaintext initial password is printed to Render logs only once, when the account is first created. Copy it from the first successful deploy logs.
- Tokens expire after eight hours. The dashboard keeps the token in the current browser tab's session storage.
- All admin API routes validate the signed token server-side.

Keep access to the Render logs and Neon database restricted. Do not share the generated initial administrator password.

## Render deployment

The root `render.yaml` creates one Docker web service named `r-fitness`. The multi-stage Docker build:
1. Builds the Vue app using Node.
2. Installs FastAPI runtime dependencies using Python.
3. Copies the built Vue assets into the Python image.
4. Runs Alembic migrations.
5. Creates a one-time administrator account if one does not already exist.
6. Starts Uvicorn, serving the website, admin dashboard and API from one origin.

**Only one manually supplied Render environment variable is required:**

| Variable | Value |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL pooled connection string |

Admin login defaults and signing secrets are handled by the application and persisted in Neon. No Supabase variables, frontend API URL, CORS variable, password variable or JWT variable are required for the production single-origin deployment.

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
