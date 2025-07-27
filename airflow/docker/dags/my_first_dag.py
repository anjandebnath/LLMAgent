from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedeltadefault_args = {'owner': 'airflow', 'retries': 1, 'retry_delay': timedelta(minutes=5)}
with DAG(
    dag_id='my_first_dag',
    default_args=default_args,
    description='My first Airflow DAG!',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    print_date = BashOperator(
        task_id='print_date',
        bash_command='date'
    )
    say_hello = BashOperator(
        task_id='say_hello',
        bash_command='echo "Hello, Airflow!"'
    )
    print_date >> say_hello