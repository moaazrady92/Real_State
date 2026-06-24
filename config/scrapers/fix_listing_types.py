import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from listings.models import Listing

# Fix aqarmap listings with empty listing_type based on source_url
fixed = 0
for listing in Listing.objects.filter(listing_type="", source="aqarmap"):
    if "for-sale" in listing.source_url:
        listing.listing_type = "for_sale"
    elif "for-rent" in listing.source_url:
        listing.listing_type = "for_rent"
    else:
        continue
    listing.save()
    fixed += 1

print(f"Fixed {fixed} listings")

from django.db.models import Count
print(list(Listing.objects.values("listing_type").annotate(count=Count("id"))))