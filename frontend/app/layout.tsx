import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'Lead Scraper & Outreach',
  description: 'Internal scraping and outreach toolkit',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 min-h-screen">
        <main className="max-w-5xl mx-auto py-10 px-4">{children}</main>
      </body>
    </html>
  );
}
