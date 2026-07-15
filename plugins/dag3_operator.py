from airflow.sdk import BaseOperator
from sqlalchemy import Column, Integer, VARCHAR, create_engine, Float, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from airflow.models import Connection
import requests
import pandas as pd
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    current_date = Column(TIMESTAMP, nullable=False, index=True)
    currency = Column(VARCHAR(50), nullable=False)
    value = Column(Float, nullable=False)


class ExampleOperator(BaseOperator):
    def __init__(self,
                 postgres_conn: Connection,
                 curr: dict,
                 **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.postgres_conn = postgres_conn
        self.curr = curr
        self.SQLAlCHEMY_DATABASE_URL = f'postgresql://{postgres_conn.login}:{postgres_conn.password}@{postgres_conn.host}:{postgres_conn.port}/{postgres_conn.schema}'


    def execute(self, context):
        engine = create_engine(self.SQLAlCHEMY_DATABASE_URL)
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session_local = SessionLocal()
        api_key = 'ddb492c0da9cf50e186c97bb'

        URL = rf'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        r = requests.get(url=URL)
        result = r.json()

        df = pd.DataFrame(columns=('current_date', 'currency', 'value'))

        for curr_name in self.curr:
            df.loc[len(df)] = [datetime.fromtimestamp(result['time_last_update_unix']),
                               f'{curr_name}',
                               result['conversion_rates'][f'{curr_name}']]

        objects = [Currency(current_date=row['current_date'], currency=row['currency'], value=row['value']) for
                   index, row in df.iterrows()]
        session_local.add_all(objects)
        session_local.commit()




