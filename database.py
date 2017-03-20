from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from config.DB_config import db_connection_info

db_con = db_connection_info['uri']

engine = create_engine(db_con, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 테이블 생성
    Base.metadata.create_all(engine)