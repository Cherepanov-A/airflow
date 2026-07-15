from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk.bases.hook import BaseHook
from plugins.dag_sensor import CheckTableSensor

connection = BaseHook.get_connection('main_postgresql_connection')

default_args = {
    'owner': 'winter',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 15),
    # 'retry_delay':timedelta(minutes=0.1)
}

with DAG(
        'dag4',
        default_args=default_args,
        description='Sensor used',
        schedule='0 * * * *',  # Запуск раз в час
        # start_date=datetime(2026, 7, 15),
        catchup=False
) as dag:

    # 3. Определение задач (Tasks)
    t1 = BashOperator(
        task_id='task1',
        bash_command='python3 /home/ubuntuuser/airflow/scripts/dag4/task1.py' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port}',
        dag=dag)

    t2 = CheckTableSensor(
        task_id='check_mutations',
        timeout=1000,
        mode='reschedule',
        poke_interval=10,
        conn=connection,
        table_name='currency',
        dag=dag)

    t3 = BashOperator(
        task_id='task3',
        bash_command='python3 /home/ubuntuuser/airflow/scripts/dag1/task3.py',
        dag=dag)

    for i in (4,5,6,7):
        some_task=BashOperator(
        task_id=f'task{str(i)}',
        bash_command='python3 /home/ubuntuuser/airflow/scripts/dag1/task2.py' +f'--host {connection.host} --dbname {connection.schema} --user {connection.login} --jdbc_password {connection.password} --port {connection.port}',
        dag=dag)
        t3 >> some_task

    # 4. Установка зависимостей (Порядок выполнения)
    t1 >> t2 >> t3
