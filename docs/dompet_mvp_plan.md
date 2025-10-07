# Dompet MVP Delivery Plan

## Vision & Product North Star
Dompet is the always-on CFP-grade financial copilot for consumers in Malaysia and, eventually, Southeast Asia. The MVP must prove that we can:

1. **Aggregate** multi-source transaction data (bank, credit card, e-wallet) with minimal friction.
2. **Analyse** cashflow health in real-time and surface actionable insights that feel like a human financial planner.
3. **Engage** users across mobile (iOS/Android) and web with a conversational, agent-driven experience inspired by Ollama's clean UI and progressive disclosure patterns.
4. **Monetise** via an affordable freemium tier while building trust to convert to paid advisory bundles.

## Agentic Flow Architecture
```
User Input (chat / upload / form)
        │
        ▼
Conversation Orchestrator ──► Memory & Profile Store
        │                           │
        ▼                           ▼
Task Planner (LLM)          Document Ingestion & Normalisation
        │                           │
        ├────► Insight Engine ◄─────┘
        │
        ▼
Recommendation Composer ──► Multichannel UI (iOS, Android, Web)
```

### Key Components
- **Conversation Orchestrator**: Handles multimodal inputs. MVP uses a deterministic rules + LLM approach with guardrails.
- **Task Planner**: Uses a cost-optimised local/hosted model to determine the next best action (e.g., request missing info, summarise month, forecast).
- **Document Ingestion**: Normalises CSV / PDF statements via templated parsers, stores structured transactions, and maintains provenance.
- **Insight Engine**: Generates financial health metrics, spending categorisation, and income opportunities.
- **Recommendation Composer**: Applies compliance templates (CFP tone) before surfacing to the user.

## Technology Stack Choices (MVP)
| Layer | Choice | Rationale |
| --- | --- | --- |
| Backend | FastAPI + SQLModel + SQLite (upgradeable to PostgreSQL) | Lightweight, async-ready, low cost |
| Data Processing | Pandas + rule-based categoriser | Fast iteration, works on CSV exports |
| LLM | Open-source small LLM (e.g., Llama 3 8B via Ollama) for on-device, fallback to hosted GPT-4o mini for accuracy | Balances cost & quality |
| Frontend | React Native + Expo (mobile), Next.js (web) | Code sharing, Ollama-like UI styling |
| Infrastructure | Render/Fly.io for API, Supabase for auth/storage, Railway for staging | Minimises DevOps overhead |

## Delivery Roadmap (Agentic Flow)
1. **Week 0-1 – Foundation**
   - Finalise compliance requirements with Malaysian regulators.
   - Stand up FastAPI backend (this repo) with ingestion, insights, recommendations.
   - Create synthetic datasets for QA.
2. **Week 2 – Conversational Layer**
   - Integrate chat planner (LangGraph or guidance) with deterministic fallbacks.
   - Implement memory schema (user profile, goals, obligations).
3. **Week 3 – Frontend Shell**
   - Build shared design system referencing Ollama's minimalist interface.
   - Hook up authentication (Supabase magic link + biometric on mobile).
4. **Week 4 – Closed Beta Prep**
   - Add bank/e-wallet connectors via file upload and manual entry.
   - Conduct user testing with 20 Malaysian beta users.
   - Instrument analytics (PostHog) & error reporting (Sentry).
5. **Week 5+ – Launch Readiness**
   - Automate categorisation with ML fine-tuning on local data.
   - Expand to SEA banks, integrate open finance APIs where viable.

## Operational Playbook
- **COO Priorities**: Define SLAs (upload <10s, insights <5s), monitor ingestion success rate, manage support queue.
- **Tech KPIs**: Daily active users, transactions ingested per user, insight click-through, premium conversion.
- **Compliance**: Data residency in Malaysia (deploy on AWS ap-southeast-1). Implement PDPA-compliant consent and deletion workflows.

## Monetisation Strategy
- **Freemium** (RM0):
  - Manual uploads, monthly cashflow report, spending alerts (email).
- **Dompet Plus** (RM19/mo or RM199/yr):
  - Automated categorisation, personalised savings plan, unlimited chat with CFP-calibrated agent, priority support.
- **Dompet Pro** (RM59/mo):
  - Couples/family accounts, investment tracking, quarterly live CFP session (partner network).
- **SEA Expansion**: Price in local currency with PPP adjustments; partner with employers for payroll deduction.

## Cost Model (12-month MVP)
- Backend hosting (Render/Fly): ~USD 50/mo staging + prod.
- Database (Supabase Pro): USD 25/mo.
- LLM inference: Start with Ollama self-hosted (GPU lease ~USD 0.6/hr during peak) + fallback GPT-4o mini (USD 150/mo cap).
- Storage (Backblaze B2): USD 5/mo for documents.
- Monitoring: Sentry (USD 29/mo), PostHog free tier initially.
Total operating cost ≈ USD 260/mo (~RM 1,200) during MVP.

## Beta & Production Checklist
- ✅ GDPR/PDPA consent screens.
- ✅ Role-based access for internal staff (CFP reviewers).
- ✅ Red-team prompts for hallucination/financial misguidance.
- ✅ Incident response runbook (data breach, downtime).
- ✅ Customer support playbook (24h response SLA).

## Next Steps for CEO
- Approve pricing tiers & cost ceiling.
- Secure partnerships with Malaysian banks/e-wallets for data access.
- Recruit 20 beta testers (mix of salaried, gig workers, families).
- Align marketing narrative around "Dompet = Your CFP in the pocket".
