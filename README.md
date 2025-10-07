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
- `docs/dompet_mvp_plan.md` – Delivery roadmap, monetisation strategy, and operational plan for the Dompet MVP.

## Next Steps
Refer to the delivery plan for week-by-week priorities, compliance checklist, and monetisation assumptions tailored to Malaysia and future SEA expansion.
