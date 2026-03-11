from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'suresh',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['your_email@example.com'], # Update with your email
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'banking_dbt_transformation',
    default_args=default_args,
    description='Run dbt transformations in the dbt_runner container',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['banking', 'dbt', 'transformation'],
) as dag:

    # 1. Check connectivity to the warehouse
    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command='docker exec dbt_runner dbt debug',
    )

    # 2. Run the models (Bronze -> Silver -> Gold)
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='docker exec dbt_runner dbt run',
        sla=timedelta(minutes=30)
    )

    # 3. Run data quality tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='docker exec dbt_runner dbt test',
    )

    # Setting up the dependency chain
    dbt_debug >> dbt_run >> dbt_test