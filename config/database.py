from dotenv import load_dotenv
import os
from sqlmodel import Field, Session, SQLModel, create_engine

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, SQLALCHEMY_DATABASE_URL)}"

engine = create_engine(database_url, echo=True, connect_args={"check_same_thread": False})

SessionLocal = Session(engine)

# Base = declarative_base()