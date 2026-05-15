"""HTTP calls to the DB Timetables API."""
import logging
from datetime import datetime, timedelta
import requests

from .config import DB_API_BASE_URL, DB_API_HEADERS

log = logging.getLogger(__name__)


def fetch_plan(eva: str, dt: datetime) -> str:
    """Fetch one hour's planned timetable for a station. Returns raw XML."""
    url = f"{DB_API_BASE_URL}/plan/{eva}/{dt.strftime('%y%m%d')}/{dt.strftime('%H')}"
    r = requests.get(url, headers=DB_API_HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def fetch_plan_window(eva: str, hours_ahead: int = 6) -> list[str]:
    """Fetch /plan for the current hour + the next N hours. Returns list of XML strings."""
    now = datetime.now()
    xml_texts = []
    for offset in range(hours_ahead + 1):
        try:
            xml_texts.append(fetch_plan(eva, now + timedelta(hours=offset)))
        except requests.HTTPError as e:
            log.warning(f"Plan fetch failed for hour +{offset}: {e}")
    return xml_texts


def fetch_changes(eva: str) -> str:
    """Fetch the full changes feed for a station. Returns raw XML."""
    url = f"{DB_API_BASE_URL}/fchg/{eva}"
    r = requests.get(url, headers=DB_API_HEADERS, timeout=30)
    r.raise_for_status()
    return r.text