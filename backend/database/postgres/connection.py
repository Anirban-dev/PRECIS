from sqlalchemy import create_engine

DATABASE_URL = (

    "postgresql://postgres:"
    "password@localhost:5432/precis"
)

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_size=20,

    max_overflow=40
)