from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.db import Base


class ScrapeRecord(Base):
    __tablename__ = "scrape_records"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, nullable=False)

    title = Column(String, nullable=True)

    headings = Column(Text, nullable=True)

    paragraphs = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
