# DEPENDENCIES
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
# SELF PROJECT IMPORTS
import models
from connection import SessionLambda, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class CostumerBase(BaseModel):
    name: str
    last_name: str
    age: int

class PhonesBase(BaseModel):
    costumer_id: int
    phone: str


def __get_db__():
    db = SessionLambda()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(__get_db__)]