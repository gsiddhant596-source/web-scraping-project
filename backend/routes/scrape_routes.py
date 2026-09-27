from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controllers.scrape_controller import (
    handle_scrape_request,
    handle_scrape_history,
    handle_scrape_by_id,
    handle_delete_scrape,
    handle_search_scrapes
)
from database.db import get_db
from models.scrape_model import ScrapeRequest


router = APIRouter(
    prefix="/api/scrape",
    tags=["Scraping"]
)


@router.get("/")
def scrape_home():
    return {
        "message": "Scraping route is working!"
    }


@router.post("/")
def scrape_website(
    request: ScrapeRequest,
    db: Session = Depends(get_db)
):
    return handle_scrape_request(
        str(request.url),
        db
    )
@router.get("/history")
def scrape_history(
    db: Session = Depends(get_db)
):
    return handle_scrape_history(db)


@router.get("/search")
def search_scrapes(
    query: str,
    db: Session = Depends(get_db)
):
    return handle_search_scrapes(
        query,
        db
    )


@router.get("/{record_id}")
def scrape_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    return handle_scrape_by_id(
        record_id,
        db
    )
@router.delete("/{record_id}")
def delete_scrape(
    record_id: int,
    db: Session = Depends(get_db)
):
    return handle_delete_scrape(
        record_id,
        db
    )
