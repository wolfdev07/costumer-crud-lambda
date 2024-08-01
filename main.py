from fastapi import FastAPI, HTTPException, Depends, status
from mangum import Mangum
from pydantic import BaseModel, Field, validator
from typing import Annotated
from sqlalchemy.orm import Session
import models
from connection import SessionLambda, engine


app = FastAPI()
handler = Mangum(app)
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
@app.get("/", status_code=status.HTTP_200_OK)
async def index():
    return {
            "info": "Welcome to the API, read the documentation for more details",
            "link": "https://github.com/wolfdev07/costumer-crud-lambda"
            }

# CREAR CLIENTE
@app.post("/costumers", status_code=status.HTTP_201_CREATED)
async def create_costumer(costumer: CostumerBase, db: db_dependency):
    # Extraer y limpiar datos del JSON
    costumer_dict = costumer.dict_for_costumer
    phone_dict = costumer.dict_for_phone

    instance = db.query(models.Phones).filter(models.Phones.phone == phone_dict["phone"]).first()
    if instance is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The phone number is already registered")
    
    # Crear el nuevo cliente
    new_costumer = models.Costumer(**costumer_dict)
    db.add(new_costumer)
    db.commit()
    db.refresh(new_costumer)

    # Guardar el teléfono
    phone_dict["costumer_id"] = new_costumer.id
    new_phone = models.Phones(**phone_dict)
    db.add(new_phone)
    db.commit()

    return {
        "id": new_costumer.id,
        "nombre": new_costumer.name,
        "apellido": new_costumer.last_name,
        "edad": new_costumer.age,
        "teléfono": int(new_phone.phone)
    }



# LISTAR CLIENTES
@app.get("/costumers/{phone}", status_code=status.HTTP_200_OK)
async def get_costumers(phone: int, db: db_dependency):
    # BUSCAR EL USUARIO
    instance = db.query(models.Phones).filter(models.Phones.phone == str(phone)).first()

    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    costumers =db.query(models.Costumer).filter(models.Costumer.id == instance.costumer_id).first()
    return {
        "id": costumers.id,
        "nombre": costumers.name,
        "apellido": costumers.last_name,
        "edad": costumers.age,
        "teléfono": int(instance.phone)
    }



# ACTUALIZAR EL CLIENTE
@app.put("/costumers/{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_costumer(phone: int, costumer: CostumerBase, db: db_dependency):
    # ACTUALIZAR EL USUARIO
    instance = db.query(models.Phones).filter(models.Phones.phone == str(phone)).first()
    
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    costumer_dict = costumer.dict_for_costumer
    phone_dict = costumer.dict_for_phone
    costumer =db.query(models.Costumer).filter(models.Costumer.id == instance.costumer_id).first()
    
    costumer.name = costumer_dict["name"]
    costumer.last_name = costumer_dict["last_name"]
    costumer.age = costumer_dict["age"]
    instance.phone = phone_dict["phone"]
    db.commit()

    return {
            "msg": "Record updated successfully",
            "name": costumer.name,
            "last_name": costumer.last_name,
            "age": costumer.age,
            "phone": int(instance.phone)
            }



# ELIMINAR EL CLIENTE
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