"""
Starter scraper for business leads.
- Uses SERP API (if key available) to seed candidate domains.
- Falls back to simple Google query URLs (non-headless) for quick demos.
- Crawls candidate pages and extracts emails/phones/social links.
"""
from __future__ import annotations

import argparse
import os
import re
import time
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl

load_dotenv()

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(r"\+?\d[\d\s().-]{7,}\d")
USER_AGENT = os.getenv("SCRAPER_USER_AGENT", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
SERP_API_KEY = os.getenv("SERP_API_KEY")


class Lead(BaseModel):
    business_name: Optional[str] = None
    industry: str
    city: str
    website_url: Optional[HttpUrl] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    contact_name: Optional[str] = None
    instagram_handle: Optional[str] = None
    tiktok_handle: Optional[str] = None
    youtube_handle: Optional[str] = None
    source_url: Optional[str] = None
    status: str = "new"


@dataclass
class PageResult:
    url: str
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    social_links: List[str] = field(default_factory=list)
    title: Optional[str] = None


class Scraper:
    def __init__(self, industry: str, city: str):
        self.industry = industry
        self.city = city
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def search_domains(self) -> List[str]:
        if SERP_API_KEY:
            return self._search_serp_api()
        return self._search_fallback()

    def _search_serp_api(self) -> List[str]:
        query = f"{self.industry} in {self.city}"
        params = {"engine": "google", "q": query, "api_key": SERP_API_KEY}
        resp = self.session.get("https://serpapi.com/search", params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        links = [item.get("link") for item in data.get("organic_results", []) if item.get("link")]
        return list(dict.fromkeys(links))[:25]

    def _search_fallback(self) -> List[str]:
        query = f"{self.industry} {self.city}".replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        resp = self.session.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        anchors = soup.select("a")
        links = []
        for a in anchors:
            href = a.get("href", "")
            if href.startswith("/url?q="):
                target = href.split("/url?q=")[1].split("&")[0]
                links.append(target)
        return list(dict.fromkeys(links))[:15]

    def crawl(self, url: str) -> PageResult:
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException:
            return PageResult(url=url)

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        emails = list(dict.fromkeys(EMAIL_REGEX.findall(text)))
        phones = list(dict.fromkeys(PHONE_REGEX.findall(text)))
        socials = [a.get("href") for a in soup.select("a") if a.get("href", "").lower().startswith(("https://www.instagram.com", "https://www.tiktok.com", "https://www.youtube.com", "https://www.facebook.com", "https://x.com"))]
        title_tag = soup.find("title")
        return PageResult(url=url, emails=emails, phones=phones, social_links=socials, title=title_tag.text if title_tag else None)

    def normalize_lead(self, result: PageResult) -> Lead:
        return Lead(
            business_name=result.title,
            industry=self.industry,
            city=self.city,
            website_url=result.url,
            email=result.emails[0] if result.emails else None,
            phone=result.phones[0] if result.phones else None,
            instagram_handle=self._pick_handle(result.social_links, "instagram"),
            tiktok_handle=self._pick_handle(result.social_links, "tiktok"),
            youtube_handle=self._pick_handle(result.social_links, "youtube"),
            source_url=result.url,
        )

    def _pick_handle(self, links: Iterable[str], platform: str) -> Optional[str]:
        for link in links:
            if platform in link:
                return link
        return None

    def run(self) -> List[Lead]:
        leads: List[Lead] = []
        for idx, domain in enumerate(self.search_domains()):
            result = self.crawl(domain)
            lead = self.normalize_lead(result)
            if lead.email or lead.phone:
                leads.append(lead)
            time.sleep(1.5)
        return leads


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape business leads by industry and city")
    parser.add_argument("--industry", required=True)
    parser.add_argument("--city", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scraper = Scraper(args.industry, args.city)
    leads = scraper.run()
    for lead in leads:
        print(lead.model_dump())


if __name__ == "__main__":
    main()
