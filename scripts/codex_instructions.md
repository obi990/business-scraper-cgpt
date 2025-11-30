# Implementation Guide

## Priorities
1. Wire backend REST endpoints (FastAPI or Flask) using models in `docs/api-design.md`.
2. Connect Supabase via service role key for server-to-server operations.
3. Add Gmail OAuth and bulk send logic with batching + retries.
4. Harden scraping with rotating user-agents, robots.txt checks, and optional Playwright for resistant sites.

## Backend Tips
- Keep scraper isolated; enqueue jobs (e.g., RQ/Redis) for long-running scrapes.
- Normalize leads before insert, deduplicate by domain/phone, and store scrape job stats.
- Render templates with merge variables via Jinja2.

## Frontend Tips
- Use React Query for `/leads`, `/templates`, and `/outreach/logs` data.
- Provide preview and test-send flows before bulk send.
- Add CSV export by calling `/leads/export` and streaming response.

## DevOps
- Use `.env.local` for frontend (Next.js) and `.env` for backend secrets.
- Add GitHub Actions for lint/test; defer heavy e2e until Playwright scraper is ready.

## Definition of Done
- Scrape job produces leads in DB within 90 seconds for common industries/cities.
- Outreach logs every message with Gmail ID, status, and timestamp.
- Templates render correctly for at least 3 merge variables (business_name, city, website_url).
