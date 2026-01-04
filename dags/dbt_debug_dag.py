from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


# define the paths for the dbt project and pfofile
DBT_PROJECT_DIR = "/opt/airflow/dbt/mbdp_dbt_project"
DBT_PROFILES_DIR = "/opt/airflow/dbt/" 

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    'dbt_debug_dag',
    default_args = default_args,
    description= "A simple DAG to verify dbt setup",
    schedule_interval= None,
    catchup= False,
) as dag:
    
    # Task to run dbt debug
    test_dbt_connection = BashOperator(
        task_id = "run_dbt_debug",
        bash_command = f"dbt debug --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )
    
    test_dbt_connection 