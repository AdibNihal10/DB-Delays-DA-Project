"""End-to-end pipeline: fetch from API, parse, write to Postgres."""
import logging
from .api import fetch_plan_window, fetch_changes
from .parsers import parse_plan_xml, parse_fchg_xml
from .db import (
    get_engine, create_tables, upsert_stations,
    write_planned_stops, write_changed_stops,
)
from .config import STATIONS


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )


def run_one_station(engine, eva: str) -> dict:
    """Run the pipeline for one station. Returns counts for logging."""
    log = logging.getLogger("pipeline")
    log.info(f"=== {eva} ({STATIONS[eva]['name']}) ===")

    # Plan
    plan_xmls = fetch_plan_window(eva, hours_ahead=6)
    plan_rows = []
    for xml in plan_xmls:
        plan_rows.extend(parse_plan_xml(xml))
    plan_written = write_planned_stops(engine, plan_rows, eva)
    log.info(f"Planned stops written: {plan_written}")

    # Changes
    fchg_xml = fetch_changes(eva)
    fchg_rows = parse_fchg_xml(fchg_xml)
    chg_written = write_changed_stops(engine, fchg_rows, eva)
    log.info(f"Changed stops written: {chg_written}")

    return {"plan": plan_written, "changes": chg_written}


def main():
    setup_logging()
    log = logging.getLogger("pipeline")
    log.info("Pipeline starting.")

    engine = get_engine()
    create_tables(engine)
    upsert_stations(engine, STATIONS)

    totals = {"plan": 0, "changes": 0}
    for eva in STATIONS:
        counts = run_one_station(engine, eva)
        totals["plan"] += counts["plan"]
        totals["changes"] += counts["changes"]

    log.info(f"Pipeline finished. Total — plan: {totals['plan']}, changes: {totals['changes']}")


if __name__ == "__main__":
    main()