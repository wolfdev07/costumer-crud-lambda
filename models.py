from sqlalchemy import String, Integer, Column, CheckConstraint
from connection import Base

# TABLE OF CUSTOMERS WITH PERSONAL DATA
class Costumer(Base):
    __tablename__ = "costumers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_name = Column(String(50))
    age = Column(Integer, CheckConstraint('age >= 18 AND age <= 100', name='age_between_18_and_100'))

# TABLE OF CLIENTS FOR PHONES
class Phones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    costumer_id = Column(Integer)
    phone = Column(String(15), unique=True)