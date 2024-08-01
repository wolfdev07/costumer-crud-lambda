import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE_OPS")

engine = create_engine(URL_DATABASE)
SessionLambda = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()