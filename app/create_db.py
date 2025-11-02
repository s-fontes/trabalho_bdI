from sqlalchemy import text
from db.database import Base, engine
from db import models  # importa os modelos para registrar as tabelas

if __name__ == "__main__":
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS biblioteca"))
    Base.metadata.create_all(bind=engine)

