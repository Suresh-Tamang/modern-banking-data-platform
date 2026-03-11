from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'suresh',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'branch_etl_dag',
    default_args=default_args,
    description='Trigger ETL inside an existing running container',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['banking', 'bash', 'docker-compose'],
) as dag:

    # Triggering the command in the already-running container
    execute_branch_etl = BashOperator(
        task_id='execute_branch_etl_command',
        bash_command='docker exec python_etl bash -c "python -m src.branch_main --source api --load-mode copy"',
        sla=timedelta(minutes=20)
    )

    execute_branch_etl