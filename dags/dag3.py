from datetime import datetime
from airflow import DAG
from airflow.sdk.bases.hook import BaseHook
from plugins.dag3_operator import ExampleOperator


connection= BaseHook.get_connection('main_postgresql_connection')

default_args = {
    'owner': 'winter',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 13),
    # 'retry_delay':timedelta(minutes=0.1)
}


with DAG(
    'dag3',
    default_args=default_args,
    description='Простой пример DAG с Bash и Python операторами',
    schedule='0 * * * *',  # Запуск раз в час
    # start_date=datetime(2026, 7, 15),
    catchup=False
) as dag:

    # 3. Определение задач (Tasks)
    t1 = ExampleOperator(
            task_id='task1',
            postgres_conn=connection,
            curr={'EUR'},
            dag=dag)

    t2 = ExampleOperator(
            task_id='task2',
            postgres_conn=connection,
            curr={'RUB'},
            dag=dag)

    # 4. Установка зависимостей (Порядок выполнения)
    t2 >> t1