from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import BaseHook

connection= BaseHook.get_connection('main_postgresql_connection')

default_args = {
    'owner': 'winter',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 7),
    # 'retry_delay':timedelta(minutes=0.1)
}


with DAG(
    'example_simple_dag',
    default_args=default_args,
    description='Простой пример DAG с Bash и Python операторами',
    schedule='0 * * * *',  # Запуск раз в час
    start_date=datetime(2026, 7, 6),
    catchup=False

) as dag:

    # 3. Определение задач (Tasks)
    t1 = BashOperator(
            task_id='task1',
            bash_command='python3 /home/ubuntuuser/airflow/scripts/dag1/task1.py --date {{ hs }} ' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port}',
            dag=dag)

    t2 = BashOperator(
            task_id='task2',
            bash_command='python3 /home/ubuntuuser/airflow/scripts/dag1/task2.py --date {{ hs }} ' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port}',
            dag=dag)

    # 4. Установка зависимостей (Порядок выполнения)
    t1 >> t2