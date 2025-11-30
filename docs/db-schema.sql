-- Supabase-ready schema for lead scraping & outreach

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

create table if not exists leads (
    id uuid primary key default uuid_generate_v4(),
    business_name text not null,
    industry text not null,
    city text not null,
    website_url text,
    email text,
    phone text,
    contact_name text,
    instagram_handle text,
    tiktok_handle text,
    youtube_handle text,
    source_url text,
    status text not null default 'new',
    deleted_at timestamp with time zone,
    created_at timestamp with time zone not null default now(),
    last_contacted_at timestamp with time zone,
    constraint leads_unique unique (website_url, phone)
);

create table if not exists email_templates (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    subject text not null,
    body text not null,
    variables text[] default array[]::text[],
    created_at timestamp with time zone not null default now(),
    updated_at timestamp with time zone not null default now()
);

create table if not exists outreach_logs (
    id uuid primary key default uuid_generate_v4(),
    lead_id uuid references leads(id),
    template_id uuid references email_templates(id),
    gmail_message_id text,
    recipient text not null,
    status text not null,
    error text,
    sent_at timestamp with time zone not null default now()
);

create table if not exists scrape_jobs (
    id uuid primary key default uuid_generate_v4(),
    industry text not null,
    city text not null,
    filters jsonb default '{}'::jsonb,
    status text not null default 'pending',
    stats jsonb default '{}'::jsonb,
    created_at timestamp with time zone not null default now(),
    completed_at timestamp with time zone
);

-- Views for quick filtering
create or replace view leads_contactable as
select * from leads where email is not null or phone is not null;

-- Soft delete helper
create or replace function soft_delete_lead(target uuid) returns void as $$
begin
  update leads set deleted_at = now() where id = target;
end;
$$ language plpgsql;
