# Lead Scraping & Automated Outreach Application

This repository contains the foundational design and starter implementation for an internal web application that scrapes business leads, stores them in a structured database, and supports templated outreach via Gmail.

## Contents
- `docs/architecture.md` — high-level system architecture with workflows.
- `docs/api-design.md` — REST API design for scraping, lead management, templates, and outreach.
- `docs/db-schema.sql` — Supabase-ready Postgres schema.
- `backend/` — Python scraping starter and utility scripts.
- `frontend/` — Next.js boilerplate UI for scraping, lead browsing, and email template drafting.
- `scripts/codex_instructions.md` — implementation guide for expanding the MVP.

## Quick Start
1. Install backend dependencies (creates a local SQLite DB at `backend/leads.db`):
1. Install backend dependencies:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the backend API locally (no hosted website needed):
   ```bash
   uvicorn backend.app:app --reload
   ```
   - Health check: `GET http://localhost:8000/health`
   - Trigger a scrape and persist leads: `POST http://localhost:8000/scrape {"industry": "restaurants", "city": "Austin"}`
   - Browse leads: `GET http://localhost:8000/leads`
3. Run a one-off scrape via CLI (prints normalized leads to stdout):
   ```bash
   python -m backend.scraper --industry "restaurants" --city "Austin, TX"
   ```
4. Install frontend dependencies and start the dev server:
2. Run a sample scrape (prints normalized leads to stdout):
   ```bash
   python scraper.py --industry "restaurants" --city "Austin, TX"
   ```
3. Install frontend dependencies and start the dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

> Note: API keys (SERP, Supabase, Google) should be provided via environment variables; see `.env.example` files in the respective services.
