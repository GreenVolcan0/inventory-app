from sqlalchemy import create_engine, func
from typing import Annotated
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column

from app.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True)]
int_uniq = Annotated[int, mapped_column(unique=True)]

Base = declarative_base()

def get_db():
    db = session_local()
    try: yield db
    finally: db.close()