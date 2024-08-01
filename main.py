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

# AGREGAR VALIDACION PARA DUCPLICADOS
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

# LISTAR TODOS LOS CLIENTES
@app.get("/costumers/{phone}", status_code=status.HTTP_200_OK)
async def get_costumers(phone: int, db: db_dependency):
    instance = db.query(models.Phones).filter(models.Phones.phone == str(phone)).first()
    costumers =db.query(models.Costumer).filter(models.Costumer.id == instance.costumer_id).first()
    return {
        "id": costumers.id,
        "nombre": costumers.name,
        "apellido": costumers.last_name,
        "edad": costumers.age,
        "teléfono": instance.phone
    }

@app.put("/costumers/{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_costumer(phone: int, costumer: CostumerBase, db: db_dependency):
    # ACTUALIZAR EL USUARIO
    instance = db.query(models.Phones).filter(models.Phones.phone == str(phone)).first()
    costumers =db.query(models.Costumer).filter(models.Costumer.id == instance.costumer_id).first()


@app.delete("/costumers/{phone}", status_code=status.HTTP_200_OK)
async def delete_costumer(phone: int, db: db_dependency):
    # ELIMINAR EL USUARIO
    instance = db.query(models.Phones).filter(models.Phones.phone == str(phone)).first()
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    costumers =db.query(models.Costumer).filter(models.Costumer.id == instance.costumer_id).first()
    db.delete(costumers)
    db.delete(instance)
    db.commit()
    return {
            "msg" : "Record deleted successfully.", 
            "id": costumers.id,
            "name": costumers.name,
            "last_name": costumers.last_name,
            "age": costumers.age,
            "phone": int(instance.phone)
            }