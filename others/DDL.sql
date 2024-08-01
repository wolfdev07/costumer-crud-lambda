CREATE TABLE costumers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    last_name VARCHAR(50),
    age INTEGER CHECK (age >= 18 AND age <= 100)
)
CREATE TABLE phones (
    id INTEGER PRIMARY KEY,
    costumer_id INTEGER,
    phone VARCHAR(15) UNIQUE
)
