# DEPENDENCIES
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, validator
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
# SELF PROJECT IMPORTS
import models
from connection import SessionLambda, engine


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class NameCostumer(BaseModel):
    nombre: str
    apellido: str

class CostumerBase(BaseModel):
    nombreCliente: NameCostumer
    telefono: int
    edad: int = Field(..., ge=18, le=100)

    @validator('telefono')
    def validate_telefono(cls, v):
        # Verificar que el número de teléfono tenga exactamente 10 dígitos
        if len(str(v)) != 10:
            raise ValueError('The phone number must be exactly 10 digits long.')
        return v

    @property
    def dict_for_costumer(self):
        return {
            "name": self.nombreCliente.nombre,
            "last_name": self.nombreCliente.apellido,
            "age": self.edad
        }
    
    @property
    def dict_for_phone(self):
        return {
            "phone": str(self.telefono)
        }


def __get_db__():
    db = SessionLambda()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(__get_db__)]


# ROUTES
@app.post("/costumers", status_code=status.HTTP_201_CREATED)
async def create_costumer(costumer: CostumerBase, db: db_dependency):
    # Extraer y limpiar datos del JSON
    costumer_dict = costumer.dict_for_costumer
    phone_dict = costumer.dict_for_phone

    # Crear el nuevo cliente
    new_costumer = models.Costumer(**costumer_dict)
    db.add(new_costumer)
    db.commit()
    db.refresh(new_costumer)

    # Guardar el teléfono
    phone_dict["costumer_id"] = new_costumer.id
    new_phone = models.Phones(**phone_dict)
    try:
        db.add(new_phone)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The phone number is already registered")

    return {
        "id": new_costumer.id,
        "nombre": new_costumer.name,
        "apellido": new_costumer.last_name,
        "edad": new_costumer.age,
        "teléfono": new_phone.phone
    }


@app.get("/costumers", status_code=status.HTTP_200_OK)
async def get_costumers(db: db_dependency):
    costumers =db.query(models.Costumer).all()
    response = []
    for costumer in costumers:
        print(costumer)
        phone = db.query(models.Phones).filter(models.Phones.costumer_id == costumer.id).first()
        print(phone.phone)
        response.append(costumer)
    return response