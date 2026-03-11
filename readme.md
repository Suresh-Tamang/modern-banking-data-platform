# Modern Banking Data Platform

A complete end-to-end data engineering solution for a banking domain built on Airflow, Postgres (metadata and warehouse), dbt, and Python-based ETL chunks.

## Project overview

Components:
- `postgres`: Airflow + Superset metadata database
- `warehouse_postgres`: dedicated analytics warehouse
- `airflow`: orchestration (DAGs in `airflow/dags`)
- `superset`: visualization and BI
- `python_etl`: Python ETL service (`pipeline/src`) for accounts, branches, customers, loans, transactions
- `dbt`: transformation pipelines in `dbt/modern_banking_warehouse`

## Repository structure

- `airflow/` - DAG definitions and Airflow logs
- `db/` - persisted PostgreSQL data directories
- `dbt/` - dbt project and models
- `pipeline/` - ETL code, settings, configuration
- `scripts/` - helper scripts (init-db)
- `docker-compose.yaml` - container definitions
- `requirements.txt` - Python dependencies for ETL container

## Configuration

### Settings
- `pipeline/config/settings.yaml`: tables, data sources (file/api/db), default load mode, key columns.

### Locally hosted api for this project
- Mock API: https://github.com/Suresh-Tamang/banking-rest-api (locally host this repo for api)
### Environment variables
- `pipeline/.env` (loaded by `python_etl`):
  - `POSTGRES_DSN=postgresql+psycopg2://warehouse:warehouse@warehouse_db:5432/warehouse`
  - `API_BASE_URL=http://.../api/`
  - `API_KEY=...`

## Docker setup

From project root:

```bash
docker compose up -d
```

Services will be available on:
- Airflow: http://localhost:8080 (admin/admin)
- Superset: http://localhost:8088 (admin/admin)
- Warehouse Postgres: localhost:5433

Inspect logs:

```bash
docker compose logs -f airflow
docker compose logs -f python_etl
```

Stop / remove:

```bash
docker compose down -v
```

##  ETL pipeline execution

ETL jobs are in `pipeline/src` and support `--source` (`api`/`file`/`db`) with `--load-mode` (`copy`/`upsert`).

Example:

```bash
docker compose exec python_etl python -m src.account_main --source file --load-mode upsert
docker compose exec python_etl python -m src.branch_main --source api --load-mode upsert
```

Replace `account_main` with `customer_main`, `loan_main`, `transaction_main` as needed.

##  dbt transformation

Start the dbt container:

```bash
docker compose exec dbt /bin/sh
```

Then inside container:

```bash
cd /usr/app/dbt/modern_banking_warehouse
dbt deps
dbt seed
dbt run
dbt test
```

##  Data sources

- CSV source path: `pipeline/data/transactions.csv` (configured in `settings.yaml`)
- API endpoints are configured in `settings.yaml` under `sources.api`
- db source query: `SELECT * FROM public.latest_users ...` (configured in `sources.db.query`)

##  Notes

- Airflow DAGs orchestrate pipelines from `airflow/dags/*.py`.
- ETL transform functions are in `pipeline/src/etl/transform/core.py`.
- Data loader supports Postgres COPY + upsert.

---

