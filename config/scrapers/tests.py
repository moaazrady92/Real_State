from aqarmap_scraper import AqarmapScraper

scraper = AqarmapScraper(
    location_path="for-sale/property-type/alexandria/sydy-bshr/sydy-bshr-qbly/cairo-st",
    max_pages=1
)
results = scraper.scrape()

for r in results:
    print(r)

print(f"\nTotal scraped: {len(results)}")