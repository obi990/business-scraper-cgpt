import React from 'react';

type Lead = {
  id: string;
  business_name?: string;
  website_url?: string;
  email?: string;
  city?: string;
  industry?: string;
  status?: string;
};

export function LeadTable({ leads }: { leads: Lead[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="text-left">
            <th className="border-b border-slate-200 py-2">Business</th>
            <th className="border-b border-slate-200 py-2">Contact</th>
            <th className="border-b border-slate-200 py-2">Location</th>
            <th className="border-b border-slate-200 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id} className="align-top">
              <td className="border-b border-slate-100 py-2">
                <div className="font-medium">{lead.business_name ?? 'Unknown'}</div>
                {lead.website_url && (
                  <a href={lead.website_url} className="text-slate-600 text-xs" target="_blank" rel="noreferrer">
                    {lead.website_url}
                  </a>
                )}
              </td>
              <td className="border-b border-slate-100 py-2">
                <div>{lead.email ?? 'No email yet'}</div>
              </td>
              <td className="border-b border-slate-100 py-2">
                <div>{lead.city ?? 'n/a'}</div>
                <div className="text-xs text-slate-600">{lead.industry}</div>
              </td>
              <td className="border-b border-slate-100 py-2">
                <span className="rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-700">{lead.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
