from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG('dbt_workflow',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /workspaces/dbt-ELT-payments-data/pymnts_elt_dbt && dbt run'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /workspaces/dbt-ELT-payments-data/pymnts_elt_dbt && dbt test'
    )

    dbt_run >> dbt_test
