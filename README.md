# Dompet MVP Backend

This repository contains the technical foundation for the Dompet personal finance copilot MVP. It includes a FastAPI backend for ingesting financial statements, generating cashflow insights, and serving recommendations, plus documentation of the agentic delivery plan.

## Getting Started
1. **Install dependencies**
   ```bash
   cd dompet_backend
   pip install -e .[dev]
   ```
2. **Initialise the database**
   ```bash
   python -c "from dompet_backend.app.services.database import init_db; init_db()"
   ```
3. **Run the API**
   ```bash
   uvicorn dompet_backend.app.main:app --reload
   ```
4. **Run tests**
   ```bash
   pytest
   ```

## Project Structure
- `dompet_backend/app` – FastAPI application modules (API routes, services, models).
- `dompet_backend/tests` – Unit tests for ingestion and insight services.
- `frontend` – Week 3 shared design system and Supabase auth utilities for the cross-platform shell.
- `docs/dompet_mvp_plan.md` – Delivery roadmap, monetisation strategy, and operational plan for the Dompet MVP.
- `docs/week3-4_delivery.md` – Summary of the frontend shell and beta-prep execution.

## Key API Routes

- `POST /auth/magic-link/verify` – Validates Supabase magic link tokens.
- `POST /auth/biometric/enrol` – Registers biometric devices tied to Supabase sessions.
- `POST /connectors/{user_id}` – Registers bank/e-wallet connectors and enables manual entry.
- `POST /connectors/{user_id}/{connector_id}/manual` – Stores manual transactions against a connector.
- `POST /beta/testers` – Manages the closed beta cohort with quota enforcement.

## Next Steps
Refer to the delivery plan for week-by-week priorities, compliance checklist, and monetisation assumptions tailored to Malaysia and future SEA expansion.
