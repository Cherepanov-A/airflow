import argparse
from datetime import datetime
import requests
import pandas as pd
from babel.numbers import validate_currency
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
parser.add_argument('--URL', dest='URL')
parser.add_argument('--jdbc_api_key', dest='jdbc_api_key')
parser.add_argument('--curr_name', dest='curr')
args = parser.parse_args()

v_host = str(args.host)
v_dbname = str(args.dbname)
v_user = str(args.user)
v_password = str(args.jdbc_password)
v_port = str(args.port)
v_api_key=str(args.jdbc_api_key)
v_URL=str(args.URL)
v_curr=dict(args.curr)

SQLAlCHEMY_DATABASE_URL = f'postgresql://{v_user}:{v_password}@{v_host}:{v_port}/{v_dbname}'


api_key= v_api_key
r=requests.get(url=v_URL)
result=r.json()

df=pd.DataFrame(columns= ('current_date', 'currency', 'value'))

df.loc[len(df)] = [datetime.fromtimestamp(result['time_last_update_unix']),
                f'{v_curr}',
                result['conversion_rates'][f'{v_curr}']]


engine = create_engine(SQLAlCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session_local = SessionLocal()
objects = [Currency(current_date=row['current_date'], currency=row['currency'],  value=row['value']) for index, row in df.iterrows()]
session_local.add_all(objects)
session_local.commit()
