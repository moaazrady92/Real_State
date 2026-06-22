from celery import shared_task
from .services import run_aqarmap_scraper


# A few seed locations to scrape on a schedule — expand this list as needed
AQARMAP_LOCATIONS = [
    "for-sale/property-type/cairo",
    "for-rent/property-type/cairo",
    "for-sale/property-type/giza",
    "for-rent/property-type/giza",
    "for-sale/property-type/alexandria",
    "for-rent/property-type/alexandria",
]


@shared_task
def scrape_aqarmap_location(location_path, max_pages=3):
    run = run_aqarmap_scraper(location_path, max_pages=max_pages)
    return {
        "location": location_path,
        "status": run.status,
        "found": run.listings_found,
        "created": run.listings_created,
        "updated": run.listings_updated,
    }


@shared_task
def scrape_all_aqarmap():
    """Fan-out task: schedules one sub-task per location."""
    for location in AQARMAP_LOCATIONS:
        scrape_aqarmap_location.delay(location, max_pages=3)