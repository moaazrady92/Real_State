import django
import os, sys
import socket
from pathlib import Path

# 1. Add paths to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(CONFIG_DIR))

# 2. Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from scrapers.services import run_nawy_scraper


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """Quick pre-check to verify if your machine actually has internet access."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


print("=== Running Nawy Live Integration Check ===")

# 3. Guard against offline status before running the heavy scraper
if not check_internet_connection():
    print("❌ Critical Error: No internet connection detected on your machine.")
    print("Please check your Wi-Fi, Ethernet, or DNS settings and try again.")
    sys.exit(1)

try:
    # 4. Execute the scraper block safely
    run = run_nawy_scraper(max_pages=2)

    # 5. Provide a cleaner, highly-readable status report
    if run.status == "success" and run.listings_found == 0:
        print("\n⚠️  Scraper ran successfully but found 0 listings.")
        print("This usually means the target website blocked the connection, or its HTML structure changed.")
    else:
        print(f"\n📊 Result: Nawy → [{run.status.upper()}]")
        print(f"   • Listings Discovered : {run.listings_found}")
        print(f"   • Database Created    : {run.listings_created}")
        print(f"   • Database Updated    : {run.listings_updated}")

    if run.error_message:
        print(f"\n❌ Scraper Internal Error Message: {run.error_message}")

except Exception as e:
    print(f"\n💥 The script itself crashed completely: {e}")
