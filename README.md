# Costumer CRUD API

**Costumer Management API** es una API RESTfull diseñada para gestionar clientes mediante operaciones de creación, lectura, actualización y eliminación (CRUD). Esta API está construida utilizando FastAPI y se despliega en AWS Lambda para aprovechar su escalabilidad y bajo coste. La API es accesible a través de API Gateway en el siguiente endpoint:

**Endpoint base:** `https://3ag4fajio1.execute-api.us-east-2.amazonaws.com/api-v1`

## Tecnologías Utilizadas

- **FastAPI:** Framework moderno y rápido para construir APIs en Python.
- **Pydantic:** Validación de datos utilizando modelos tipados.
- **SQLAlchemy:** ORM para interactuar con la base de datos.
- **AWS Lambda:** Computación serverless para desplegar y ejecutar la API.
- **AWS API Gateway:** Interfaz para exponer la API y gestionar las solicitudes HTTP.
- **Mangum:** Adaptador para que FastAPI funcione en entornos serverless como AWS Lambda.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- **models.py:** Define los modelos de datos utilizando SQLAlchemy.
- **connection.py:** Gestiona la conexión con la base de datos.
- **main.py:** Contiene las rutas y la lógica de la API.
- **README.md:** Documento de referencia para entender el proyecto.

## Endpoints Disponibles

### 1. **Crear Cliente**

**POST** `/costumers`

Crea un nuevo cliente con los datos proporcionados. Verifica que el número de teléfono no esté registrado previamente.

- **Cuerpo de la solicitud:**
  ```json
  {
    "nombreCliente": {
      "nombre": "Juan",
      "apellido": "Pérez"
    },
    "telefono": 1234567890,
    "edad": 30
  }

- **Respuesta exitosa (201):**
 ```json
  {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "teléfono": 1234567890
  }

### 2. **Listar Cliente por Teléfono**

**GET** `/costumers/{phone}`

Obtiene la información del cliente asociado al número de teléfono proporcionado.

- **Parámetros:**
  - `phone`: Número de teléfono del cliente.

- **Respuesta exitosa (200):**
  ```json
  {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "teléfono": 1234567890
  }
