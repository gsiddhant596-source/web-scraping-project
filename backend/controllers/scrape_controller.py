import json
import requests

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.repository import (
    save_scrape_record,
    get_scrape_history,
    get_scrape_by_id,
    delete_scrape_record,
    search_scrape_records
)

from services.scraper_service import scrape_website_data


def handle_scrape_request(url: str, db: Session):

    try:

        scraped_data = scrape_website_data(url)

        record = save_scrape_record(
            db,
            scraped_data
        )

        return {
            "message": "Website scraped and saved successfully",
            "record_id": record.id,
            "data": scraped_data
        }

    except requests.Timeout:

        raise HTTPException(
            status_code=504,
            detail="The website took too long to respond."
        )

    except requests.HTTPError as error:

        if error.response is not None:

            status_code = error.response.status_code

            raise HTTPException(
                status_code=status_code,
                detail=f"The website returned HTTP {status_code}."
            )

        raise HTTPException(
            status_code=502,
            detail="The website returned an HTTP error."
        )

    except requests.ConnectionError:

        raise HTTPException(
            status_code=502,
            detail="Could not connect to the website."
        )

    except requests.RequestException:

        raise HTTPException(
            status_code=502,
            detail="An error occurred while contacting the website."
        )

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred on the server."
        )


def handle_scrape_history(db: Session):

    records = get_scrape_history(db)

    history = []

    for record in records:

        history.append({
            "id": record.id,
            "url": record.url,
            "title": record.title,
            "headings": json.loads(record.headings)
                if record.headings else [],
            "paragraphs": json.loads(record.paragraphs)
                if record.paragraphs else [],
            "created_at": record.created_at
        })

    return history


def handle_scrape_by_id(record_id: int, db: Session):

    record = get_scrape_by_id(
        db,
        record_id
    )

    if record is None:

        raise HTTPException(
            status_code=404,
            detail="Scrape record not found."
        )

    return {
        "id": record.id,
        "url": record.url,
        "title": record.title,
        "headings": json.loads(record.headings)
            if record.headings else [],
        "paragraphs": json.loads(record.paragraphs)
            if record.paragraphs else [],
        "created_at": record.created_at
    }


def handle_delete_scrape(record_id: int, db: Session):

    record = delete_scrape_record(
        db,
        record_id
    )

    if record is None:

        raise HTTPException(
            status_code=404,
            detail="Scrape record not found."
        )

    return {
        "message": "Scrape record deleted successfully",
        "record_id": record_id
    }


def handle_search_scrapes(query: str, db: Session):

    records = search_scrape_records(
        db,
        query
    )

    results = []

    for record in records:

        results.append({
            "id": record.id,
            "url": record.url,
            "title": record.title,
            "headings": json.loads(record.headings)
                if record.headings else [],
            "paragraphs": json.loads(record.paragraphs)
                if record.paragraphs else [],
            "created_at": record.created_at
        })

    return results
