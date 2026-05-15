# DB Delays — Real-Time Deutsche Bahn Delay Analytics

A data pipeline that ingests live train data from the official Deutsche Bahn API,
stores it in PostgreSQL, transforms it with dbt, and serves analytics through a
Streamlit dashboard.

## Status

🚧 In progress. Currently:

- ✅ Authenticated against the official DB Timetables API
- ✅ Parsed planned timetable + live changes feed (XML)
- ✅ Computed real delays from joined plan/change data
- ⬜ Persistent storage in PostgreSQL
- ⬜ Scheduled ingestion via Prefect
- ⬜ dbt transformations
- ⬜ Streamlit dashboard
- ⬜ Deployment

## Stack

- **Python 3.12** with `uv` for dependency management
- **PostgreSQL** for the warehouse
- **Prefect** for orchestration
- **dbt** for transformations
- **Streamlit** for the dashboard

## Data source

Deutsche Bahn API Marketplace — Timetables API. Free tier, requires a free
developer account at https://developers.deutschebahn.com.

## Setup

```bash
uv sync
cp .env.example .env  # then fill in DB_CLIENT_ID and DB_API_KEY
```

## Notebook tour

`notebooks/01_explore_api.ipynb` — initial API exploration, schema discovery,
first delay computations.