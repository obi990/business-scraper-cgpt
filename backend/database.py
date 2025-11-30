import os
import uuid
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import Column, DateTime, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./leads.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
Base = declarative_base()


class LeadRecord(Base):
    __tablename__ = "leads"
    __table_args__ = (
        UniqueConstraint("website_url", name="uq_leads_website"),
        UniqueConstraint("email", name="uq_leads_email"),
        UniqueConstraint("phone", name="uq_leads_phone"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_name = Column(String, nullable=True)
    industry = Column(String, nullable=False)
    city = Column(String, nullable=False)
    website_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    instagram_handle = Column(String, nullable=True)
    tiktok_handle = Column(String, nullable=True)
    youtube_handle = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    status = Column(String, nullable=False, default="new")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_contacted_at = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
