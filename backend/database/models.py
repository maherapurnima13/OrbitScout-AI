from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class IntelligenceReport(Base):

    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(String)

    summary = Column(Text)

    insights = Column(Text)