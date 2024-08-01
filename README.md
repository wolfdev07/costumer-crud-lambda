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

### 2. **Listar Cliente por Teléfono**

**GET** `/costumers/{phone}`

Obtiene la información del cliente asociado al número de teléfono proporcionado.

- **Parámetros:**
  - `phone`: Número de teléfono del cliente.

- **Respuesta exitosa (200):**
  - `id`, `nombre`, `apellido`, `edad`, `teléfono`

### 3. **Actualizar Cliente**

**PUT** `/costumers/{phone}`

Actualiza la información de un cliente existente utilizando su número de teléfono.

- **Cuerpo de la solicitud:**
  - `nombreCliente` (nombre y apellido), `telefono`, `edad`

- **Respuesta exitosa (202):**
  - `msg`, `name`, `last_name`, `age`, `phone`

### 4. **Eliminar Cliente**

**DELETE** `/costumers/{phone}`

Elimina un cliente de la base de datos utilizando su número de teléfono.

- **Parámetros:**
  - `phone`: Número de teléfono del cliente.

- **Respuesta exitosa (200):**
  - `msg`, `id`, `name`, `last_name`, `age`, `phone`

## Ejecución Local

Para ejecutar este proyecto localmente:

1. Clona este repositorio.
2. Instala las dependencias necesarias utilizando `pip install -r requirements.txt`.
3. Configura la base de datos y crea las tablas necesarias.
4. Ejecuta la aplicación con `uvicorn main:app --reload`.

## Despliegue en AWS Lambda

Este proyecto está configurado para ejecutarse en AWS Lambda utilizando `Mangum` como adaptador. Para desplegar:

1. Crea una función Lambda en AWS.
2. Sube el código y las dependencias empaquetadas como un archivo ZIP.
    `pip3 install -t dependencies -r requirements.txt`
    `(cd dependencies; zip ../aws_lambda_artifact.zip -r .)`
    `zip aws_lambda_artifact.zip -u main.py`
3. Configura el API Gateway para exponer los endpoints.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un *issue* antes de enviar un *pull request*.

## Licencia

Este proyecto está bajo la licencia [GPL-3.0](LICENSE).