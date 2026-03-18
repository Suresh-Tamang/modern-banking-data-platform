# Modern Banking Data Platform - Runbook

## Table of Contents

1. Project Overview
2. Prerequisites
3. Architecture
4. Setup and Installation
5. Running the Platform
6. Common Operations
7. Troubleshooting
8. Monitoring and Logs
9. Development Workflow
10. Data Management

---

## 1. Project Overview

The Modern Banking Data Platform (MBDP) is a comprehensive data engineering solution designed to simulate how financial institutions collect, process, and manage large volumes of transactional data using modern data pipeline practices.

### Key Features

- ETL Pipeline: Extracts banking data from multiple sources (APIs, CSV, databases)
- Orchestration: Airflow-based workflow automation with daily scheduled pipelines
- Data Warehouse: PostgreSQL-based analytics warehouse for aggregated data
- Transformations: dbt models for data modeling and transformations
- Visualization: Superset integration for business intelligence and reporting

### Supported Data Entities

- Accounts: Banking account information
- Branches: Branch/location data
- Customers: Customer profiles and demographics
- Loans: Loan products and terms
- Transactions: Individual transaction records

---

## 2. Prerequisites

### System Requirements

- Docker Desktop or Docker Engine (20.10+)
- Docker Compose (1.29+)
- At least 4GB RAM available for containers
- Linux, macOS, or Windows with WSL2
- Git (for version control)

### Environment Setup

- Clone the repository:
  ```bash
  git clone <repository-url>
  cd modern-banking-data-platform
  ```

### External API Setup (Optional)

To use the API data source, set up the mock banking API:

```bash
git clone https://github.com/Suresh-Tamang/banking-rest-api
cd banking-rest-api
# Follow setup instructions in the API repository
```

Configure the API URL and credentials:
- Edit `pipeline/config/settings.yaml`
- Set `API_BASE_URL` to your API endpoint
- Set `API_KEY` in environment variables

---

## 3. Architecture

### Container Services

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  postgres (metadata_db)         warehouse_postgres           │
│  - Airflow metadata             - Analytics warehouse        │
│  - Superset configuration       - Persisted data             │
│  - Port: 5432                   - Port: 5433                 │
│                                                               │
│  airflow (webserver & scheduler)                             │
│  - DAG orchestration                                         │
│  - Workflow scheduling                                       │
│  - Port: 8080                                                │
│                                                               │
│  python_etl                     dbt                          │
│  - ETL jobs                     - Data transformations      │
│  - Data ingestion               - Model validation          │
│                                                               │
│  superset                                                    │
│  - BI and visualization                                      │
│  - Port: 8088                                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Multiple Sources
    |
    +-- API Endpoints
    |   └-> Configured in settings.yaml
    |
    +-- CSV Files
    |   └-> pipeline/data/transactions.csv
    |
    +-- Existing Database
    |   └-> SQL queries in settings.yaml
    |
    v
Python ETL Service
    |
    v
Metadata Database (postgres)
    |
    v
Warehouse Database (warehouse_postgres)
    |
    v
dbt Transformations
    |
    v
Analytics Models/Reports
    |
    v
Superset Dashboard
```

### Project Structure

```
modern-banking-data-platform/
├── airflow/                      # Airflow configuration
│   ├── dags/                     # DAG definitions
│   │   ├── account_etl_dag.py
│   │   ├── branch_etl_dag.py
│   │   ├── customer_etl_dag.py
│   │   ├── loan_etl_dag.py
│   │   ├── transaction_etl_dag.py
│   │   └── dbt_dag.py
│   ├── logs/                     # DAG execution logs
│   └── plugins/                  # Custom Airflow plugins
│
├── db/                           # Database volumes
│   ├── postgres_data/            # Metadata database
│   └── postgres_warehouse/       # Warehouse database
│
├── dbt/                          # dbt project
│   ├── profiles.yml              # dbt connection config
│   └── modern_banking_warehouse/ # dbt models
│       ├── dbt_project.yml
│       ├── models/               # Transform logic
│       ├── tests/                # Data quality tests
│       └── seeds/                # Seed data
│
├── pipeline/                     # Python ETL service
│   ├── config/
│   │   ├── settings.yaml         # Data source & table config
│   │   └── logging.yaml          # Logging configuration
│   ├── data/                     # Sample data files
│   │   └── transactions.csv
│   └── src/                      # ETL scripts
│       ├── account_main.py
│       ├── branch_main.py
│       ├── customer_main.py
│       ├── loan_main.py
│       ├── transaction_main.py
│       ├── models.py             # SQLAlchemy models
│       ├── config.py             # Configuration loader
│       └── logging_setup.py
│
├── scripts/                      # Helper scripts
│   └── init-db.sh                # Database initialization
│
├── docker-compose.yaml           # Container orchestration
├── Dockerfile                    # Python ETL image
├── requirements.txt              # Python dependencies
└── RUNBOOK.md                    # This file
```

---

## 4. Setup and Installation

### Step 1: Initialize the Project

From the project root directory:

```bash
# Clone and enter the repository
cd modern-banking-data-platform

# Verify Docker is running
docker ps
```

### Step 2: Build and Start Containers

```bash
# Build and start all services (runs in background)
docker compose up -d

# Wait for services to initialize (30-60 seconds)
docker compose ps
```

Expected output should show all services with "healthy" or "running" status.

### Step 3: Verify Service Health

```bash
# Check service status
docker compose ps

# View initialization logs
docker compose logs postgres
docker compose logs airflow

# Wait until you see "Airflow Webserver is running"
```

### Step 4: Access Web Interfaces

After services are healthy, access these URLs:

- Airflow Webserver: http://localhost:8080
  - Username: admin
  - Password: admin

- Superset BI: http://localhost:8088
  - Username: admin
  - Password: admin

- Database Warehouse: localhost:5433
  - Username: warehouse
  - Password: warehouse

### Step 5: Set Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
cat > .env << 'EOF'
POSTGRES_DSN=postgresql+psycopg2://warehouse:warehouse@warehouse_db:5432/warehouse
API_BASE_URL=http://localhost:3000/api/
API_KEY=your-api-key-here
EOF
```

### Step 6: Initial Data Loading

If using the warehouse for the first time, initialize the schema:

```bash
# View the database init script
cat scripts/init-db.sh

# This runs automatically during docker compose up
# Check if tables were created
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "\dt"
```

---

## 5. Running the Platform

### Option A: Fully Automatic (Recommended)

Airflow DAGs run on a schedule. By default, all ETL DAGs are configured to run daily at midnight UTC.

To verify scheduled runs:

1. Go to Airflow at http://localhost:8080
2. Click on each DAG (account_etl_dag, customer_etl_dag, etc.)
3. Check the "Tree View" to see past and future runs

### Option B: Manual ETL Execution

#### Run Individual ETL Jobs

Execute a single ETL job directly:

```bash
# Account ETL from API source with copy mode
docker compose exec python_etl python -m src.account_main --source api --load-mode copy

# Branch ETL from API source with upsert mode
docker compose exec python_etl python -m src.branch_main --source api --load-mode upsert

# Customer ETL from file source
docker compose exec python_etl python -m src.customer_main --source file --load-mode copy

# Loan ETL from database source
docker compose exec python_etl python -m src.loan_main --source db --load-mode upsert

# Transaction ETL from file source
docker compose exec python_etl python -m src.transaction_main --source file --load-mode copy
```

#### ETL Command Parameters

- `--source`: Data source type
  - `api`: External REST API
  - `file`: CSV file (configured in settings.yaml)
  - `db`: Existing PostgreSQL database

- `--load-mode`: Data loading strategy
  - `copy`: Replace all existing data (truncate and reload)
  - `upsert`: Merge with existing data (insert new, update existing based on key columns)

#### Run dbt Transformations

Connect to dbt container:

```bash
docker compose exec dbt /bin/sh
```

Inside the container, run:

```bash
# Navigate to dbt project
cd /usr/app/dbt/modern_banking_warehouse

# Install dbt packages (first time only)
dbt deps

# Load seed data (reference data)
dbt seed

# Execute transformation models
dbt run

# Run data quality tests
dbt test

# Generate documentation
dbt docs generate

# View dbt status
dbt debug
```

#### Run Specific dbt Models

```bash
# Inside dbt container
dbt run --select model_name
dbt test --select model_name
```

#### Trigger DAGs Manually from Airflow UI

1. Go to http://localhost:8080
2. Click on a DAG name (e.g., "account_etl_dag")
3. Click the "Trigger DAG" button (play icon)
4. Optionally configure run parameters in the triggered dialog
5. Monitor execution in the DAG's tree/Gantt view

---

## 6. Common Operations

### Working with Data

#### Load Data into Warehouse

```bash
# Load all entity types from API
docker compose exec python_etl python -m src.account_main --source api --load-mode upsert
docker compose exec python_etl python -m src.branch_main --source api --load-mode upsert
docker compose exec python_etl python -m src.customer_main --source api --load-mode upsert
docker compose exec python_etl python -m src.loan_main --source api --load-mode upsert
docker compose exec python_etl python -m src.transaction_main --source file --load-mode copy
```

#### Query Warehouse Data

Connect directly to the warehouse database:

```bash
# Access PostgreSQL warehouse
docker compose exec warehouse_postgres psql -U warehouse -d warehouse

# Inside psql shell
SELECT COUNT(*) FROM public.accounts;
SELECT COUNT(*) FROM public.transactions;
SELECT * FROM public.branches LIMIT 5;
```

#### Clear All Data

```bash
# Clear warehouse data (destructive)
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "
TRUNCATE TABLE public.accounts CASCADE;
TRUNCATE TABLE public.branches CASCADE;
TRUNCATE TABLE public.customers CASCADE;
TRUNCATE TABLE public.loans CASCADE;
TRUNCATE TABLE public.transactions CASCADE;
"
```

### Managing Containers

#### View Running Containers

```bash
docker compose ps
```

#### View Container Logs

```bash
# Real-time logs for specific service
docker compose logs -f airflow
docker compose logs -f python_etl
docker compose logs -f dbt

# View logs with timestamps
docker compose logs -f --timestamps airflow

# Tail last 100 lines
docker compose logs --tail 100 airflow
```

#### Restart Services

```bash
# Restart a specific service
docker compose restart airflow

# Restart all services
docker compose restart

# Stop services
docker compose stop

# Start services
docker compose start
```

#### Reset Everything

Use only when you need to start fresh:

```bash
# Stop and remove containers, networks, and volumes
docker compose down -v

# Remove all data (database volumes)
rm -rf db/postgres_data/*
rm -rf db/postgres_warehouse/*

# Restart everything
docker compose up -d
```

### Configuration Management

#### Modify ETL Settings

```bash
# Edit data source configuration
nano pipeline/config/settings.yaml

# Changes take effect on next ETL run
# No container restart needed
```

#### Configure Logging

Edit logging configuration:

```bash
nano pipeline/config/logging.yaml
```

Supported log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

---

## 7. Troubleshooting

### Issue: Services Fail to Start

#### Symptom: Docker compose up exits with errors

**Solution:**

```bash
# Check Docker daemon
docker ps

# View detailed error logs
docker compose logs

# Verify disk space
df -h

# Try rebuilding containers
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Issue: Airflow Webserver Unreachable

#### Symptom: http://localhost:8080 connection refused

**Solution:**

```bash
# Check if container is running
docker compose ps airflow

# View Airflow logs
docker compose logs airflow

# Restart Airflow
docker compose restart airflow

# Wait 30 seconds and try again
sleep 30 && curl http://localhost:8080
```

### Issue: ETL Job Stuck or Hanging

#### Symptom: ETL job doesn't complete or runs indefinitely

**Solution:**

```bash
# Check container logs
docker compose logs python_etl

# Check memory usage
docker stats python_etl

# Kill stuck process and restart
docker compose restart python_etl

# Manually check connection to warehouse
docker compose exec python_etl python -c "
from pipeline.src.config import load_config
config = load_config()
print(f'DSN: {config[\"database\"][\"dsn\"]}')"
```

### Issue: Database Connection Errors

#### Symptom: "could not connect to server" error

**Solution:**

```bash
# Verify database container is healthy
docker compose ps warehouse_postgres

# Check if port 5433 is accessible
telnet localhost 5433

# Verify credentials
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "SELECT 1"

# Check environment variables in python_etl
docker compose exec python_etl env | grep POSTGRES
```

### Issue: dbt Transformation Fails

#### Symptom: "dbt run" fails with errors

**Solution:**

```bash
# Enter dbt container
docker compose exec dbt /bin/sh

# Debug connection
dbt debug

# Check dbt packages installed
dbt deps

# Run with verbose output
dbt run --debug

# Validate YAML syntax
dbt parse
```

### Issue: Airflow DAG Not Triggering

#### Symptom: DAG scheduled but not running

**Solution:**

1. Check DAG is unpaused:
   - Go to Airflow UI: http://localhost:8080
   - Toggle DAG status to "ON" (green)

2. Check scheduler is running:
   ```bash
   docker compose logs airflow | grep scheduler
   ```

3. Check DAG parsing errors:
   ```bash
   docker compose exec airflow airflow dags list
   docker compose exec airflow airflow dags list-runs -d account_etl_dag
   ```

4. Check if next run time has passed:
   - View scheduled runs in Airflow UI
   - Check system time matches expected run time

### Issue: Out of Memory

#### Symptom: Containers killed or services crash

**Solution:**

```bash
# Check memory usage
docker stats

# Increase Docker memory allocation (desktop settings)
# Or reduce batch size in settings.yaml:
nano pipeline/config/settings.yaml
# Change: batch_size: 1000 to batch_size: 500

# Restart services
docker compose restart
```

### Issue: Permission Denied Errors

#### Symptom: "Permission denied" when accessing files

**Solution:**

```bash
# Fix directory permissions
chmod -R 755 airflow/
chmod -R 755 db/
chmod -R 755 pipeline/
chmod -R 755 dbt/

# Rebuild containers
docker compose down
docker compose up -d
```

### Issue: Port Already in Use

#### Symptom: "Port X is already allocated" error

**Solution:**

```bash
# Find what's using the port (example: 8080)
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yaml
# Change ports: ["8081:8080"] for Airflow

# Restart
docker compose up -d
```

---

## 8. Monitoring and Logs

### Airflow Monitoring

#### Check DAG Health

Go to Airflow UI: http://localhost:8080

- Tree View: Visual representation of DAG structure and run status
- Graph View: Dependency graph between tasks
- Calendar View: Historical run status by date
- Gantt View: Task execution timeline

#### Monitor Task Execution

1. Click on a DAG
2. Click on a task (blue box in tree view)
3. View task logs, try to run, or retry failed tasks

#### Check DAG Schedule

1. Airflow UI -> DAG page
2. View "Schedule" field (e.g., "Daily at 00:00")
3. Check "Last Run" and "Next Run" timestamps

### Application Logs

#### ETL Pipeline Logs

```bash
# Real-time logs
docker compose logs -f python_etl

# Specific file
cat pipeline/logs/etl.json

# Filter errors
docker compose logs python_etl | grep ERROR
```

#### dbt Logs

```bash
# Navigate to dbt logs
docker compose exec dbt ls -la /usr/app/dbt/modern_banking_warehouse/logs/

# View latest run
docker compose exec dbt dbt run --debug
```

#### Airflow Logs

```bash
# View DAG logs
ls airflow/logs/

# Check specific DAG run logs
cat airflow/logs/dag_id=account_etl_dag/run_id=scheduled__2026-03-13T00:00:00+00:00/
```

### Log Levels

Configure in `pipeline/config/logging.yaml`:

- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages (failures)
- CRITICAL: Critical failures requiring immediate attention

---

## 9. Development Workflow

### Adding a New ETL Job

1. Create a new Python script in `pipeline/src/`:
   ```bash
   cp pipeline/src/account_main.py pipeline/src/new_entity_main.py
   ```

2. Update the script with your entity logic

3. Create a corresponding DAG in `airflow/dags/`:
   ```bash
   cp airflow/dags/account_etl_dag.py airflow/dags/new_entity_etl_dag.py
   ```

4. Update DAG configuration for your entity

5. Test manually:
   ```bash
   docker compose exec python_etl python -m src.new_entity_main --source api --load-mode copy
   ```

6. Verify in Airflow UI - DAG should appear within a few seconds

### Modifying dbt Models

1. Edit or create model in `dbt/modern_banking_warehouse/models/`

2. Update YAML references if needed

3. Test changes:
   ```bash
   docker compose exec dbt dbt run --select your_model
   docker compose exec dbt dbt test --select your_model
   ```

4. Regenerate docs:
   ```bash
   docker compose exec dbt dbt docs generate
   ```

### Running Unit Tests

```bash
# Python ETL tests
docker compose exec python_etl pytest

# dbt data quality tests
docker compose exec dbt dbt test

# Specific test
docker compose exec dbt dbt test --select test_name
```

### Local Development (Without Docker)

For local Python development:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export POSTGRES_DSN="postgresql://..."
export API_BASE_URL="http://localhost:3000/api/"

# Run ETL
python -m src.account_main --source api --load-mode copy
```

---

## 10. Data Management

### Data Retention Policy

- Metadata database (airflow): Keep indefinitely
- Warehouse transactions: Keep rolling 2-year window
- ETL logs: Archive after 30 days

### Backup Strategy

#### Backup Warehouse Data

```bash
# Backup database
docker compose exec warehouse_postgres pg_dump -U warehouse warehouse > warehouse_backup.sql

# Restore database
docker compose exec -T warehouse_postgres psql -U warehouse warehouse < warehouse_backup.sql
```

#### Backup Airflow Metadata

```bash
# Backup Airflow database
docker compose exec postgres pg_dump -U airflow airflow > airflow_backup.sql
```

#### Backup dbt Project

```bash
# dbt project is version-controlled
# Ensure you commit to git
git add dbt/
git commit -m "dbt models backup"
```

### Data Validation

#### Check Data Quality

```bash
# Run dbt tests
docker compose exec dbt dbt test

# Check specific table
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "
SELECT 
    tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname='public' 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

#### Row Counts by Table

```bash
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "
SELECT 'accounts' as table_name, COUNT(*) as row_count FROM public.accounts
UNION ALL
SELECT 'branches', COUNT(*) FROM public.branches
UNION ALL
SELECT 'customers', COUNT(*) FROM public.customers
UNION ALL
SELECT 'loans', COUNT(*) FROM public.loans
UNION ALL
SELECT 'transactions', COUNT(*) FROM public.transactions;
"
```

### Troubleshooting Data Issues

#### Missing Data

1. Check ETL logs: `docker compose logs python_etl`
2. Verify source configuration: `cat pipeline/config/settings.yaml`
3. Check database connection: `docker compose exec python_etl python -m src.config`
4. Retry ETL job: `docker compose exec python_etl python -m src.account_main --source api --load-mode upsert`

#### Data Consistency Issues

1. Run dbt tests: `docker compose exec dbt dbt test`
2. Review test results for specific failures
3. Fix dbt model or source data
4. Re-run transformations

#### Duplicate Records

Use copy load mode to reload clean data:

```bash
# Clear and reload
docker compose exec python_etl python -m src.account_main --source api --load-mode copy
```

---

## Quick Reference

### Essential Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f airflow

# Run ETL
docker compose exec python_etl python -m src.account_main --source api --load-mode copy

# Run dbt
docker compose exec dbt dbt run

# Query warehouse
docker compose exec warehouse_postgres psql -U warehouse -d warehouse -c "SELECT * FROM public.accounts LIMIT 5;"

# Restart a service
docker compose restart airflow

# Check status
docker compose ps
```

### Access Credentials

- Airflow: admin / admin
- Superset: admin / admin
- Warehouse DB: warehouse / warehouse
- Metadata DB: airflow / airflow

### Critical Paths

- DAG definitions: `airflow/dags/`
- ETL scripts: `pipeline/src/`
- Configuration: `pipeline/config/settings.yaml`
- dbt models: `dbt/modern_banking_warehouse/models/`
- Database volumes: `db/`

### Support

For issues not covered in this runbook:

1. Check logs: `docker compose logs -f`
2. Review configuration: `pipeline/config/`
3. Verify Docker and system resources
4. Consult project documentation: `readme.md`
5. Review dbt documentation: `dbt/modern_banking_warehouse/README.md`

---

## Version History

- v1.0 - Initial runbook creation
- Date: March 18, 2026

---

End of Runbook
