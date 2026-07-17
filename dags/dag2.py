from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk.bases.hook import BaseHook
from airflow.sdk import Variable


api_key=Variable.get('api_key_v6')
URL=Variable.get('URL_v6')
URL = URL.replace('api_key', f'{api_key}')
connection= BaseHook.get_connection('main_postgresql_connection')

default_args = {
    'owner': 'winter',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 13),
    # 'retry_delay':timedelta(minutes=0.1)
}


with DAG(
    'example_simple_dag',
    default_args=default_args,
    description='Простой пример DAG с Bash и Python операторами',
    schedule='0 * * * *',  # Запуск раз в час
    # start_date=datetime(2026, 7, 6),
    catchup=False

) as dag:

    # 3. Определение задач (Tasks)
    t1 = BashOperator(
            task_id='task1',
            bash_command='python3 /home/ubuntuuser/airflow/scripts/dag2/task1.py --date {{ ds }} --curr_name RUB ' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port} --URL {URL} --jdbc_api_key {api_key}',
            dag=dag)

    t2 = BashOperator(
            task_id='task2',
            bash_command='python3 /home/ubuntuuser/airflow/scripts/dag2/task2.py --date {{ ds }} --curr_name EUR ' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port} --URL {URL} --jdbc_api_key {api_key}',
            dag=dag)

    # 4. Установка зависимостей (Порядок выполнения)
    t2 >> t1