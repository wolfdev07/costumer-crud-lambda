from sqlalchemy import String, Integer, Column
from connection import Base

# TABLA DE CLIENTES CON DATOS PERSONALES
class Costumer(Base):
    __tablename__ = "costumers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    age = Column(Integer)

# TABLA DE CLIENTES PARA TELÉFONOS
class Phones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    costumer_id = Column(Integer)
    phone = Column(Integer, unique=True)