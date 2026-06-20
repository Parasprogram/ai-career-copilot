import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"
)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    ca_path = os.getenv("TIDB_SSL_CA", r"C:\Users\Dell\Downloads\isrgrootx1.pem")
    if ca_path and os.path.exists(ca_path):
        connect_args = {"ssl": {"ca": ca_path}}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()