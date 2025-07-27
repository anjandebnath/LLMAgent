from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id='sample_dag',
    start_date=datetime(2025, 1, 1),
    schedule='@daily',
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Hello, Airflow!"'
    )