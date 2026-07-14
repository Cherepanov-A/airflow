
from airflow.sdk import BaseOperator

from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from airflow.models import Connection

class Base(DeclarativeBase):
    pass



class Currency(Base):
    __tablename__ = 'for_airflow_plugin'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    text_field = Column(VARCHAR(50), nullable=False)


class ExampleOperator(BaseOperator):
    def __init__(self,
                 postgre_conn: Connection,
                 text_field: str,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.postgre_conn = postgre_conn
        self.text_field = text_field
        self.SQLAlCHEMY_DATABASE_URL = f'postgresql://{postgre_conn.login}:{postgre_conn.password}@{postgre_conn.host}:{postgre_conn.port}/{postgre_conn.schema}'


    def execute(selfs, context):
        engine = create_engine(selfs.SQLAlCHEMY_DATABASE_URL)
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session_local.commit()




