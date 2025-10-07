# Dompet Frontend Shell

This directory contains the week 3 deliverable for the Dompet MVP: a shared design system inspired by Ollama's minimalist interface and client-side authentication hooks for Supabase magic link and biometric re-authentication.

## Structure

- `src/design-system` – Theme tokens, foundational components, and layout primitives.
- `src/features/auth` – Supabase helper utilities for magic link sign-in and biometric persistence.

The design system favours neutral surfaces, progressive disclosure, and generous whitespace. Components expose minimal props while enforcing consistent typography and spacing tokens.

## Getting Started

```bash
pnpm install
pnpm dev
```

Set the following environment variables for Supabase:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

Biometric helpers rely on the Web Authentication API on web and a compatible Expo module on mobile.
