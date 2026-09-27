from fastapi import FastAPI

from database.db import Base, engine
from models.scrape_record_model import ScrapeRecord

from routes.scrape_routes import router as scrape_router


app = FastAPI(
    title="Web Scraping Application",
    description="Backend API for our web scraping project",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Backend is running successfully!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(scrape_router)
