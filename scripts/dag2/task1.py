import argparse
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, VARCHAR, Float, TIMESTAMP

class Base(DeclarativeBase):
    pass

class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    current_date = Column(TIMESTAMP, nullable=False, index=True)
    currency = Column(VARCHAR(50), nullable=False)
    value = Column(Float, nullable=False)


parser=argparse.ArgumentParser()
parser.add_argument("--date", dest="date")
parser.add_argument("--host", dest="host")
parser.add_argument("--dbname", dest="dbname")
parser.add_argument("--user", dest="user")
parser.add_argument("--jdbc_password", dest="jdbc_password")
parser.add_argument("--port", dest="port")
args = parser.parse_args()

v_host = str(args.host)
v_dbname = str(args.dbname)
v_user = str(args.user)
v_password = str(args.jdbc_password)
v_port = str(args.port)

SQLAlCHEMY_DATABASE_URL = f'postgresql://{v_user}:{v_password}@{v_host}:{v_port}/{v_dbname}'
# api_key='8ed393c70b0dae5ae46912d3b6958926'

api_key='ddb492c0da9cf50e186c97bb'
curr={'RUB'}
# URL=rf'https://api.currencylayer.com/live?access_key={api_key}&source=USD&currencies={curr}'
URL=rf'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
r=requests.get(url=URL)
result=r.json()

df=pd.DataFrame(columns= ('current_date', 'currency', 'value'))

for curr_name in curr:
    df.loc[len(df)] = [datetime.fromtimestamp(result['time_last_update_unix']),
                    f'{curr_name}',
                    result['conversion_rates'][f'{curr_name}']]


engine = create_engine(SQLAlCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_local = SessionLocal()
objects = [Currency(current_date=row['current_date'], currency=row['currency'],  value=row['value']) for index, row in df.iterrows()]
session_local.add_all(objects)
session_local.commit()
