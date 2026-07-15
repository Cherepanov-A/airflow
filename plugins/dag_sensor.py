from airflow.sdk import BaseSensorOperator
from airflow.models import Connection
import pandas as pd
import psycopg2 as pg


class CheckTableSensor(BaseSensorOperator):
    poke_context_fields = ['conn', 'table_name']

    def __init__(self, conn: Connection, table_name: str, *args, **kwargs):
        self.conn = conn
        self.table_name = table_name
        super(CheckTableSensor, self).__init__(*args, **kwargs)

    def poke(self, context):
        connection = pg.connect(
            f'postgresql://{self.conn.login}:{self.conn.password}@{self.conn.host}:{self.conn.port}/{self.conn.schema}')
        df_currency = pd.read_sql(f'SELECT * FROM {self.table_name} LIMIT 1', connection)
        if len(df_currency) > 0:
            return True
        else:
            return False
