import React from 'react';

type Lead = {
  business_name?: string;
  industry?: string;
  city?: string;
  contact_name?: string;
  website_url?: string;
};

export function TemplatePreview({ template, lead }: { template: string; lead: Lead }) {
  const rendered = Object.entries(lead).reduce((body, [key, value]) => {
    return body.replaceAll(`{${key}}`, value ?? '');
  }, template);

  return (
    <div className="border border-slate-200 rounded p-3 bg-slate-50">
      <div className="text-xs text-slate-500 mb-2">Preview</div>
      <pre className="whitespace-pre-wrap text-sm text-slate-800">{rendered}</pre>
    </div>
  );
}
