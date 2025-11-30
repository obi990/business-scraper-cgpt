# API Design

## Authentication
- Internal single-user app. Protect endpoints with Supabase service key verification header (e.g., `X-Service-Key`) and Google OAuth for Gmail send operations.

## Endpoints

### Scraping
- `POST /api/scrape`
  - Body: `{ "industry": "restaurants", "city": "Austin, TX", "filters": {"has_social": true} }`
  - Response: `{ "job_id": "uuid", "estimated_seconds": 60 }`
- `GET /api/scrape/:job_id`
  - Returns job status and partial results.

### Leads
- `GET /api/leads?city=&industry=&status=&has_contact=`
  - Filters: `status` in (`new`, `contacted`, `bounced`), `has_contact` to require email/phone.
- `POST /api/leads`
  - Manual upload. Accepts array of lead objects matching schema.
- `PATCH /api/leads/:id`
  - Update status, contact info, or soft delete flag.
- `GET /api/leads/export?format=csv`
  - Streams CSV export of current filter.

### Templates
- `GET /api/templates`
- `POST /api/templates` — create template with `name`, `subject`, `body`, `variables`.
- `PATCH /api/templates/:id`
- `DELETE /api/templates/:id`
- `POST /api/templates/:id/preview` — body: `{ "lead": {...} }` returns rendered body.

### Outreach
- `POST /api/outreach/send`
  - Body: `{ "template_id": "uuid", "lead_ids": ["uuid"], "test_email": "optional" }`
  - Sends emails (test email bypasses lead logging).
- `GET /api/outreach/logs?lead_id=&status=`

## Data Models
- **Lead**: id, business_name, industry, city, website_url, email, phone, contact_name, instagram_handle, tiktok_handle, youtube_handle, source_url, created_at, last_contacted_at, status, deleted_at.
- **Template**: id, name, subject, body, variables, created_at, updated_at.
- **OutreachLog**: id, lead_id, template_id, gmail_message_id, recipient, status, error, sent_at.
- **ScrapeJob**: id, industry, city, filters, status, stats (total leads, deduped), created_at, completed_at.

## Pagination & Sorting
- Use cursor-based pagination: `?cursor=...&limit=50`.
- Sort by `created_at` or `last_contacted_at` with `?sort=created_at&order=desc`.

## Error Handling
- JSON error shape: `{ "error": "message", "code": "ERROR_CODE" }`.

## Rate Limits
- Scrape: 1 concurrent job per operator to avoid throttling.
- Outreach: default batch size 50, 2–3s delay between sends.
