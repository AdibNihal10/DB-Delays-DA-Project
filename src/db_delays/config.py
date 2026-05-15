#Configuration: loads environment variables and exposes constants.
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# DB API credentials
DB_CLIENT_ID = os.getenv("DB_CLIENT_ID")
DB_API_KEY = os.getenv("DB_API_KEY")

# Postgres connection
PG_USER = os.getenv("DB_PG_USER")
PG_PASSWORD = os.getenv("DB_PG_PASSWORD")
PG_HOST = os.getenv("DB_PG_HOST", "localhost")
PG_PORT = os.getenv("DB_PG_PORT", "5432")
PG_DATABASE = os.getenv("DB_PG_DATABASE")

POSTGRES_URL = (
    f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
)

# API constants
DB_API_BASE_URL = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
DB_API_HEADERS = {
    "DB-Client-Id": DB_CLIENT_ID,
    "DB-Api-Key": DB_API_KEY,
    "Accept": "application/xml",
}

# Stations we track (start small, expand later)
STATIONS = STATIONS = {
    "8011160": {"name": "Berlin Hbf",       "ds100": "BLS"},
    "8000261": {"name": "München Hbf",      "ds100": "MH"},
    "8000105": {"name": "Frankfurt (M) Hbf","ds100": "FF"},
    "8000207": {"name": "Köln Hbf",         "ds100": "KK"},
}