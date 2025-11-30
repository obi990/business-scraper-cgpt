'use client';

import { useState } from 'react';
import { LeadTable } from '../components/LeadTable';
import { TemplatePreview } from '../components/TemplatePreview';

export default function HomePage() {
  const [industry, setIndustry] = useState('restaurants');
  const [city, setCity] = useState('Austin, TX');
  const [templateBody, setTemplateBody] = useState(
    'Hi {business_name}, we help {industry} in {city} turn website visitors into booked calls with AI-powered video ads.'
  );

  const mockLeads = [
    {
      id: '1',
      business_name: 'Sample Kitchen',
      website_url: 'https://samplekitchen.example',
      email: 'owner@samplekitchen.example',
      city,
      industry,
      status: 'new',
    },
  ];

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold">Lead Scraper & Outreach</h1>
        <p className="text-slate-600">Scrape prospects, manage leads, and send templated outreach via Gmail.</p>
      </header>

      <section className="card">
        <h2 className="text-xl font-semibold mb-3">Scrape</h2>
        <div className="grid gap-3 md:grid-cols-2">
          <label className="flex flex-col gap-1">
            <span className="text-sm text-slate-600">Industry</span>
            <input
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="border border-slate-200 rounded px-3 py-2"
              placeholder="restaurants"
            />
          </label>
          <label className="flex flex-col gap-1">
            <span className="text-sm text-slate-600">City</span>
            <input
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="border border-slate-200 rounded px-3 py-2"
              placeholder="Austin, TX"
            />
          </label>
        </div>
        <div className="mt-3 flex gap-2">
          <button className="btn">Run scrape</button>
          <span className="text-sm text-slate-500">Jobs usually finish in 30–90s.</span>
        </div>
      </section>

      <section className="card">
        <h2 className="text-xl font-semibold mb-3">Leads</h2>
        <LeadTable leads={mockLeads} />
      </section>

      <section className="card space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Email Template</h2>
          <button className="btn">Save template</button>
        </div>
        <textarea
          className="w-full border border-slate-200 rounded px-3 py-2"
          value={templateBody}
          onChange={(e) => setTemplateBody(e.target.value)}
          rows={5}
        />
        <TemplatePreview
          template={templateBody}
          lead={{ business_name: 'Sample Kitchen', industry, city, contact_name: 'Alex' }}
        />
        <div className="flex gap-2">
          <button className="btn">Send test email</button>
          <button className="btn">Send to selected leads</button>
        </div>
      </section>
    </div>
  );
}
