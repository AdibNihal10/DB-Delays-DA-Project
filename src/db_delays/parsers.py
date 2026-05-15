"""XML parsers for /plan and /fchg responses."""
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_db_time(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.strptime(s, "%y%m%d%H%M")


def parse_plan_xml(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    rows = []
    for s in root.findall("s"):
        tl = s.find("tl")
        ar = s.find("ar")
        dp = s.find("dp")
        rows.append({
            "stop_id": s.get("id"),
            "train_category": tl.get("c") if tl is not None else None,
            "train_number": tl.get("n") if tl is not None else None,
            "operator": tl.get("o") if tl is not None else None,
            "planned_arrival": parse_db_time(ar.get("pt")) if ar is not None else None,
            "planned_arrival_platform": ar.get("pp") if ar is not None else None,
            "arrival_line": ar.get("l") if ar is not None else None,
            "arrival_path": ar.get("ppth") if ar is not None else None,
            "planned_departure": parse_db_time(dp.get("pt")) if dp is not None else None,
            "planned_departure_platform": dp.get("pp") if dp is not None else None,
            "departure_line": dp.get("l") if dp is not None else None,
            "departure_path": dp.get("ppth") if dp is not None else None,
        })
    return rows


def parse_fchg_xml(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    rows = []
    for s in root.findall("s"):
        ar = s.find("ar")
        dp = s.find("dp")
        reasons = [m.get("c") for m in s.iter("m") if m.get("t") == "d" and m.get("c")]
        rows.append({
            "stop_id": s.get("id"),
            "changed_arrival": parse_db_time(ar.get("ct")) if ar is not None and ar.get("ct") else None,
            "changed_arrival_platform": ar.get("cp") if ar is not None else None,
            "changed_departure": parse_db_time(dp.get("ct")) if dp is not None and dp.get("ct") else None,
            "changed_departure_platform": dp.get("cp") if dp is not None else None,
            "delay_codes": ",".join(sorted(set(reasons))) if reasons else None,
        })
    return rows