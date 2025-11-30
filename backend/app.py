from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database import LeadRecord, get_session
from backend.scraper import Lead, Scraper

app = FastAPI(title="Lead Scraper Backend", version="0.1.0")


class LeadCreate(BaseModel):
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


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    last_contacted_at: Optional[datetime] = None


class LeadRead(LeadCreate):
    id: str
    created_at: datetime


class ScrapeRequest(BaseModel):
    industry: str
    city: str


class ScrapeResponse(BaseModel):
    created: int
    duplicates: int


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def get_db():
    with get_session() as session:
        yield session


def record_to_schema(record: LeadRecord) -> LeadRead:
    return LeadRead(
        id=record.id,
        business_name=record.business_name,
        industry=record.industry,
        city=record.city,
        website_url=record.website_url,
        email=record.email,
        phone=record.phone,
        contact_name=record.contact_name,
        instagram_handle=record.instagram_handle,
        tiktok_handle=record.tiktok_handle,
        youtube_handle=record.youtube_handle,
        source_url=record.source_url,
        status=record.status,
        created_at=record.created_at,
        last_contacted_at=record.last_contacted_at,
    )


@app.post("/scrape", response_model=ScrapeResponse)
def scrape(req: ScrapeRequest, session: Session = Depends(get_db)) -> ScrapeResponse:
    scraper = Scraper(req.industry, req.city)
    leads = scraper.run()
    created = 0
    duplicates = 0

    for lead in leads:
        record = LeadRecord(
            business_name=lead.business_name,
            industry=lead.industry,
            city=lead.city,
            website_url=str(lead.website_url) if lead.website_url else None,
            email=lead.email,
            phone=lead.phone,
            contact_name=lead.contact_name,
            instagram_handle=lead.instagram_handle,
            tiktok_handle=lead.tiktok_handle,
            youtube_handle=lead.youtube_handle,
            source_url=lead.source_url,
            status=lead.status,
        )
        session.add(record)
        try:
            session.commit()
            session.refresh(record)
            created += 1
        except IntegrityError:
            session.rollback()
            duplicates += 1

    return ScrapeResponse(created=created, duplicates=duplicates)


@app.post("/leads", response_model=LeadRead)
def create_lead(lead: LeadCreate, session: Session = Depends(get_db)) -> LeadRead:
    record = LeadRecord(**lead.model_dump())
    session.add(record)
    try:
        session.commit()
        session.refresh(record)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Lead already exists (email/phone/website)")
    return record_to_schema(record)


@app.get("/leads", response_model=List[LeadRead])
def list_leads(
    city: Optional[str] = None,
    industry: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = Query(None, description="Search by business name or domain"),
    session: Session = Depends(get_db),
) -> List[LeadRead]:
    stmt = select(LeadRecord)
    if city:
        stmt = stmt.where(LeadRecord.city.ilike(f"%{city}%"))
    if industry:
        stmt = stmt.where(LeadRecord.industry.ilike(f"%{industry}%"))
    if status:
        stmt = stmt.where(LeadRecord.status == status)
    if search:
        stmt = stmt.where(
            or_(
                LeadRecord.business_name.ilike(f"%{search}%"),
                LeadRecord.website_url.ilike(f"%{search}%"),
                LeadRecord.email.ilike(f"%{search}%"),
            )
        )
    results = session.scalars(stmt.order_by(LeadRecord.created_at.desc())).all()
    return [record_to_schema(row) for row in results]


@app.patch("/leads/{lead_id}", response_model=LeadRead)
def update_lead(lead_id: str, payload: LeadUpdate, session: Session = Depends(get_db)) -> LeadRead:
    record = session.get(LeadRecord, lead_id)
    if not record:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_data = payload.model_dump(exclude_unset=True)
    if update_data.get("status"):
        record.status = update_data["status"]
    if update_data.get("last_contacted_at"):
        record.last_contacted_at = update_data["last_contacted_at"]

    session.add(record)
    session.commit()
    session.refresh(record)
    return record_to_schema(record)
