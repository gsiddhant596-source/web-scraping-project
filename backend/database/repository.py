import json

from sqlalchemy.orm import Session

from models.scrape_record_model import ScrapeRecord


def save_scrape_record(db: Session, scraped_data: dict):

    record = ScrapeRecord(
        url=scraped_data["url"],
        title=scraped_data["title"],
        headings=json.dumps(scraped_data["headings"]),
        paragraphs=json.dumps(scraped_data["paragraphs"])
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_scrape_history(db: Session):

    return (
        db.query(ScrapeRecord)
        .order_by(ScrapeRecord.created_at.desc())
        .all()
    )


def get_scrape_by_id(db: Session, record_id: int):

    return (
        db.query(ScrapeRecord)
        .filter(ScrapeRecord.id == record_id)
        .first()
    )


def delete_scrape_record(db: Session, record_id: int):

    record = (
        db.query(ScrapeRecord)
        .filter(ScrapeRecord.id == record_id)
        .first()
    )

    if record is None:
        return None

    db.delete(record)
    db.commit()

    return record


def search_scrape_records(db: Session, query: str):

    search_text = f"%{query}%"

    return (
        db.query(ScrapeRecord)
        .filter(
            (ScrapeRecord.url.ilike(search_text)) |
            (ScrapeRecord.title.ilike(search_text))
        )
        .order_by(ScrapeRecord.created_at.desc())
        .all()
    )
