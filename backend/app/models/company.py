from sqlalchemy import Column, Integer, String, JSON, DateTime, ARRAY
from sqlalchemy.sql import func
from app.database import Base


class Company(Base):
    # Defining the table name
    __tablename__ = "company"

    # Defining columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=None)
    documentNumber = Column(String, default=None)
    status = Column(String, default=None)
    detailsUrl = Column(String, default=None)
    filingInformation = Column(JSON, default=None)
    principalAddress = Column(String, default=None)
    mailingAddress = Column(String, default=None)
    registeredAgent = Column(JSON, default=None)
    officers = Column(ARRAY(JSON), default=None)
    annualReports = Column(ARRAY(JSON), default=None)
    documentImages = Column(ARRAY(JSON), default=None)

    # Time realted columns
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
