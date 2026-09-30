import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)


load_dotenv()


def obtener_database_url():

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if database_url:

        if database_url.startswith(
            "postgres://"
        ):
            database_url = (
                database_url.replace(
                    "postgres://",
                    "postgresql+psycopg://",
                    1
                )
            )

        elif database_url.startswith(
            "postgresql://"
        ):
            database_url = (
                database_url.replace(
                    "postgresql://",
                    "postgresql+psycopg://",
                    1
                )
            )

        return database_url


    db_user = os.getenv(
        "DB_USER"
    )

    db_password = os.getenv(
        "DB_PASSWORD"
    )

    db_host = os.getenv(
        "DB_HOST"
    )

    db_port = int(
        os.getenv(
            "DB_PORT",
            "5432"
        )
    )

    db_name = os.getenv(
        "DB_NAME"
    )


    if not all([
        db_user,
        db_password,
        db_host,
        db_name
    ]):
        raise RuntimeError(
            "No se encontró la configuración "
            "de la base de datos"
        )


    return URL.create(
        drivername="postgresql+psycopg",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )


DATABASE_URL = obtener_database_url()


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(
    DeclarativeBase
):
    pass


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()