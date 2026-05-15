"""PostgreSQL connection and write helpers."""
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from .config import POSTGRES_URL

log = logging.getLogger(__name__)

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS stations (
    eva                 TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    ds100               TEXT,
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS planned_stops (
    stop_id                     TEXT NOT NULL,
    station_eva                 TEXT NOT NULL,
    train_category              TEXT,
    train_number                TEXT,
    operator                    TEXT,
    planned_arrival             TIMESTAMP,
    planned_arrival_platform    TEXT,
    arrival_line                TEXT,
    arrival_path                TEXT,
    planned_departure           TIMESTAMP,
    planned_departure_platform  TEXT,
    departure_line              TEXT,
    departure_path              TEXT,
    fetched_at                  TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (stop_id, station_eva)
);

CREATE TABLE IF NOT EXISTS changed_stops (
    stop_id                     TEXT NOT NULL,
    station_eva                 TEXT NOT NULL,
    changed_arrival             TIMESTAMP,
    changed_arrival_platform    TEXT,
    changed_departure           TIMESTAMP,
    changed_departure_platform  TEXT,
    delay_codes                 TEXT,
    fetched_at                  TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (stop_id, station_eva, fetched_at)
);
"""


def get_engine() -> Engine:
    return create_engine(POSTGRES_URL)


def create_tables(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text(CREATE_TABLES_SQL))
    log.info("Tables ensured.")


def upsert_stations(engine: Engine, stations: dict) -> None:
    """Insert station metadata, ignoring duplicates."""
    rows = [{"eva": eva, **info} for eva, info in stations.items()]
    sql = text("""
        INSERT INTO stations (eva, name, ds100)
        VALUES (:eva, :name, :ds100)
        ON CONFLICT (eva) DO NOTHING
    """)
    with engine.begin() as conn:
        conn.execute(sql, rows)


def write_planned_stops(engine: Engine, rows: list[dict], station_eva: str) -> int:
    """Replace planned_stops for this station with the latest fetch."""
    if not rows:
        return 0
    df = pd.DataFrame(rows)
    df["station_eva"] = station_eva
    df = df.astype(object).where(df.notna(), None)
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM planned_stops WHERE station_eva = :eva"),
            {"eva": station_eva},
        )
        df.to_sql("planned_stops", conn, if_exists="append", index=False)
    return len(df)


def write_changed_stops(engine: Engine, rows: list[dict], station_eva: str) -> int:
    """Append the latest change snapshot. Historical snapshots are preserved."""
    if not rows:
        return 0
    df = pd.DataFrame(rows)
    df["station_eva"] = station_eva
    df = df.astype(object).where(df.notna(), None)
    with engine.begin() as conn:
        df.to_sql("changed_stops", conn, if_exists="append", index=False)
    return len(df)