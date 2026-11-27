# R Fitness

A gym website and lead-management dashboard for R Fitness, Uppal, Hyderabad.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Bootstrap 5
- API: FastAPI, Pydantic, SQLAlchemy 2, Alembic
- Data and identity: Supabase PostgreSQL + Supabase Auth
- Hosting: Render static site + Docker web service

## Repository layout

```text
frontend/       Vue website and admin dashboard
backend/        FastAPI application, migrations and tests
render.yaml     Render Blueprint for frontend + API
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

Set DATABASE_URL in backend/.env to a Supabase PostgreSQL connection string. The app adapts standard postgresql:// URLs to psycopg.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  
Health check: http://localhost:8000/healthz

### Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173.

Set VITE_API_BASE_URL=http://localhost:8000. To use admin login locally, set the public Supabase URL and anon/publishable key in frontend/.env.

## Supabase setup

1. Create a Supabase project.
2. In Project Settings → Database, copy a PostgreSQL connection string. Prefer the Session pooler connection string for an IPv4-only host. Keep the database password private.
3. In Project Settings → API, copy the Project URL and anon/publishable key.
4. Create an administrator in Authentication → Users. Copy that user's UUID into backend ADMIN_USER_IDS (comma-separated for multiple admins).
5. The API validates access tokens with Supabase Auth and then checks the user's UUID against ADMIN_USER_IDS. Signing in alone does not grant admin permissions.

Never use a service-role key in the browser. Never commit database passwords, access tokens, or .env files.

## Render deployment

The root render.yaml defines:
- r-fitness-web: Vue static site
- r-fitness-api: FastAPI Docker web service

Create a Blueprint from this repository in Render. Supply prompted secrets in the Dashboard.

Required API variables:
- DATABASE_URL: Supabase PostgreSQL Session pooler or supported direct connection
- SUPABASE_URL: Supabase project URL
- SUPABASE_ANON_KEY: Supabase anon/publishable key
- ADMIN_USER_IDS: approved admin UUID(s)
- CORS_ORIGINS: exact deployed frontend origin, e.g. https://r-fitness-web.onrender.com

Required frontend variables:
- VITE_API_BASE_URL: deployed API origin, e.g. https://r-fitness-api.onrender.com
- VITE_SUPABASE_URL: Supabase project URL
- VITE_SUPABASE_ANON_KEY: Supabase anon/publishable key

Vite variables are public and embedded in the browser bundle. Only put the Supabase URL and anon/publishable key in the frontend; never put database credentials or a service-role key there.

The API container applies Alembic migrations before starting Uvicorn. Render health checks use /healthz.

## Before publishing

The initial content uses the public business listing for the gym's name, address and phone. Confirm these with the owner before launch. Membership prices, exact services, trainer profiles, class schedules and Sunday hours are intentionally not invented; populate them after the owner confirms the details.

## MVP included

- Responsive public gym website
- Membership plans (no invented prices)
- Trial / membership enquiry form stored in PostgreSQL
- Supabase Auth admin sign-in
- Admin enquiry inbox with status updates
- Admin membership-plan management
- Docker, database migrations, health check and Render Blueprint

Member accounts, payments, attendance, trainer management UI and class booking are future phases.
