# GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI: API REST para Gestión de Usuarios

## Descripción de la aplicación

**device_systems** es una API REST desarrollada con **FastAPI** que permite administrar usuarios del sistema.  
Esta aplicación backend expone endpoints para **listar usuarios**, **consultar un usuario por ID**, **filtrar usuarios por rol y estado**, y **crear nuevos usuarios** con validaciones robustas.

La API está construida siguiendo los principios REST y utiliza:

- **Pydantic v2** para la validación automática de datos y definición de esquemas.
- **Parámetros de ruta** para acceder a recursos específicos.
- **Parámetros de consulta** para filtrar y personalizar respuestas.
- **Modelos de respuesta** para estandarizar la salida y ocultar información sensible.
- **Cabeceras HTTP personalizadas** para identificar la aplicación y su versión.

Este proyecto es el resultado de un reto integrador que consolida los fundamentos de FastAPI, demostrando su capacidad para crear APIs eficientes, autodocumentadas y fáciles de mantener.

---

## Instalación de dependencias

Para que la API funcione correctamente, necesitamos instalar tres componentes principales:

| Dependencia | ¿Para qué sirve? |
|---|---|
| FastAPI | Es el motor de la API. Proporciona todas las herramientas para crear los endpoints (rutas) y manejar las peticiones HTTP. |
| Uvicorn | Es el servidor que pone en marcha la API y la mantiene a la escucha de peticiones (como un recepcionista que atiende llamadas). |
| email-validator | Es una pequeña ayuda que permite verificar que los correos electrónicos tengan un formato válido (por ejemplo, que contengan un `@` y un dominio). |

Estas dependencias se instalan automáticamente con el siguiente comando:

```bash
python -m uv add fastapi uvicorn[standard] email-validator
```
![Instalacion dependencias](images/instalacion_dependencias.png)
![Instalacion uvicorn](images/instalacion_uvicorn.png)
---

## Ejecución del servidor

Una vez instaladas las dependencias, dentro de la carpeta `device_systems` ejecuta:

```bash
python -m uv run uvicorn app.main:app --
```

**Salida:**
INFO:     Will watch for changes in these directories: ['C:\\SENA\\device_systems']

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

INFO:     Started reloader process [5808] using WatchFiles

INFO:     Started server process [20468]

INFO:     Waiting for application startup.

INFO:     Application startup complete.

Acceso a la API y documentación API base: http://localhost:8000

Swagger UI (documentación interactiva): http://localhost:8000/docs

---

## Endpoints de la API

A continuación se describe cada uno de los **endpoints disponibles** en la API `device_systems`. Se incluyen los métodos HTTP, rutas, descripción, parámetros y códigos de respuesta esperados.

| Método | Ruta | Descripción | Parámetros | Códigos de respuesta |
|--------|------|-------------|------------|----------------------|
| GET | `/` | Mensaje de bienvenida a la API | Ninguno | 200 OK |
| GET | `/users` | Lista todos los usuarios (con filtros opcionales) | `role` (query, opcional, valores: `admin`, `support`, `user`)<br>`is_active` (query, opcional, `true`/`false`) | 200 OK |
| GET | `/users/{user_id}` | Obtiene un usuario por su ID | `user_id` (path, entero, requerido) | 200 OK, 404 Not Found |
| POST | `/users` | Crea un nuevo usuario | Body JSON con los campos: `name`, `email`, `role`, `is_active` | 201 Created, 400 Bad Request, 422 Unprocessable Entity |

El endpoint `GET /users` acepta `role` e `is_active` como **query parameters** (parámetros de consulta). Esto permite filtrar la lista de usuarios sin necesidad de crear múltiples rutas fijas.

---

## Ejemplos de peticiones GET y POST

###  GET /users (sin filtros)
```bash
curl -X GET "http://localhost:8000/users"
```

### GET /users con filtros
```bash
curl -X GET "http://localhost:8000/users?role=admin&is_active=true"
```

### GET /users/{user_id}
```bash
curl -X GET "http://localhost:8000/users/1"
```

### POST /users (creación válida)
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Mendoza",
    "email": "carlos@example.com",
    "role": "support",
    "is_active": true
  }'
```

### POST /users (datos inválidos – error 422)
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jo",
    "email": "correo-mal",
    "role": "superuser",
    "is_active": true
  }'
```
---

## Evidencias de pruebas con capturas de pantalla

A continuación se muestran las capturas realizadas durante las pruebas de la API `device_systems`. Cada imagen demuestra el correcto funcionamiento de los endpoints, las validaciones, el manejo de errores y las cabeceras personalizadas.

---

### 1. Documentación Swagger UI completa

![Swagger UI general](images/Swagger.png)

**Propósito:** Mostrar la interfaz autogenerada por FastAPI donde se documentan automáticamente todos los endpoints, parámetros, modelos de datos y códigos de respuesta.

**Explicación:** En `http://localhost:8000/docs` se listan los endpoints `GET /users`, `GET /users/{user_id}`, `POST /users` y el raíz `GET /`. Además, se visualizan los schemas `UserCreate`, `UserResponse`, `RoleEnum` y los errores de validación. Esta documentación es interactiva y permite probar la API directamente desde el navegador.

---

### 2. Lista inicial vacía – `GET /users`

![GET /users vacío](images/Lista_vacia.png)

**Propósito:** Verificar que al iniciar la API no hay usuarios precargados en el sistema.

**Explicación:** Inmediatamente después de que se ejecuto el servidor, se realiza una petición `GET /users` desde Insomnia. La respuesta es un arreglo vacío `[]`, lo cual es correcto porque aún no se ha creado ningún usuario.

---

### 3. Creación de usuario válido – `POST /users` (código 201)

![POST usuario válido](images/creacion_usuario.png)

**Propósito:** Demostrar que se puede registrar un nuevo usuario correctamente.

**Explicación:** Se envía una petición POST con un JSON que contiene `name`, `email`, `role` e `is_active`. FastAPI valida los datos con Pydantic, los almacena en memoria y responde con código **201 Created**. La respuesta incluye el objeto completo del usuario creado, con el `id: 3` asignado automáticamente.

---

### 4. Filtrado con query parameters – `GET /users?role=admin&is_active=true`

![GET con filtros](images/get_users_filtros..png)

**Propósito:** Comprobar que los parámetros de consulta `role` e `is_active` permiten filtrar la lista de usuarios.

**Explicación:** Se realiza `GET /users?role=admin&is_active=true`. La API retorna únicamente los usuarios cuyo rol es `admin` y que están activos. En la captura aparecen `ana rosales` (id=2) y `Jairo Corrales` (id=3), ambos administradores activos. Y los usuarios `Lucía Ruiz` que es rol `user` y `Carlos Mendoza` que es rol `support` no aparecen porque no cumplen el filtro.

---

### 5. Obtener usuario por ID existente – `GET /users/1`

![GET por ID existente](images/id_existente.png)

**Propósito:** Validar que el **path parameter** `{user_id}` funciona correctamente y retorna el recurso solicitado.

**Explicación:** Se consulta `GET /users/1`. FastAPI extrae el valor `1` de la URL. En este caso, retorna a `Carlos Mendoza` con rol `support` y código **200 OK**. Esto demuestra el correcto uso de parámetros de ruta.

---

### 6. Usuario no encontrado – `GET /users/100` (código 404)

![GET 404 no encontrado](images/usuario_no_encontrado.png)

**Propósito:** Verificar el manejo de IDs inexistentes con un error **404 Not Found** y un mensaje descriptivo.

**Explicación:** Se solicita `GET /users/100`, un ID que no existe en la base de datos. La API responde con código **404 Not Found** y el mensaje `"Usuario no encontrado"`. Este comportamiento sigue el estándar REST y permite al cliente saber que el recurso no existe sin ambigüedad.

---

### 7. Segunda creación de usuario válido – `POST /users` (código 201)

![POST segundo usuario válido](images/creacion_usuario2.png)

**Propósito:** Demostrar que se pueden crear múltiples usuarios y que el ID se incrementa correctamente.

**Explicación:** Se crea un nuevo usuario llamado `Lucía Ruiz` con rol `user`. La respuesta es **201 Created** y se le asigna el `id: 4`. Esto confirma que el contador de IDs funciona de forma incremental y que no hay conflictos entre registros.

---

### 8. Error por email duplicado – `POST /users` (código 400)

![Error email duplicado](images/error_email.png)

**Propósito:** Validar que la API rechaza un segundo registro con el mismo correo electrónico, previniendo duplicados.

**Explicación:** Se intenta crear un usuario con el email `luci@example.com` (similar al de Lucía Ruiz, pero con una letra menos). El mensaje de error es `"El email ya está registrado"`. Esto demuestra que antes de guardar, la API verifica la unicidad del email y devuelve un **400 Bad Request**.

---

### 9. Validación de nombre muy corto – `POST /users` (código 422)

![Validación nombre corto](images/nombre_corto.png)

**Propósito:** Mostrar cómo Pydantic valida que el campo `name` tenga al menos 3 caracteres.

**Explicación:** Se envía `"name": "Jo"` (solo 2 caracteres). La API responde con **422 Unprocessable Entity** y un detalle que indica: `"String should have at least 3 characters"` en la ubicación `body.name`. Esta validación automática evita nombres demasiado cortos.

---

### 10. Validación de email inválido – `POST /users` (código 422)

![Validación email inválido](images/validacion_email.png)

**Propósito:** Comprobar que el campo `email` debe tener un formato válido (con `@` y dominio).

**Explicación:** Se envía `"email": "correo-mal"` sin el símbolo `@`. Pydantic (con `EmailStr`) rechaza el valor y devuelve un error 422 con el mensaje: `"value is not a valid email address: An email address must have an @-sign."`. Esto garantiza que solo correos bien formados sean aceptados.

---

### 11. Validación de rol no permitido – `POST /users` (código 422)

![Validación rol inválido](images/validacion_rol.png)

**Propósito:** Verificar que el campo `role` solo acepte los valores `admin`, `support` o `user`.

**Explicación:** Se envía `"role": "superuser"` que no está en el `Enum`. La respuesta 422 indica: `"Input should be 'admin', 'support' or 'user'"`. Esto restringe los roles a los definidos en el sistema.

---

### 12. Cabeceras HTTP personalizadas

![Cabeceras personalizadas](images/cabeceras_personalizadas.png)

**Propósito:** Verificar que todas las respuestas incluyen las cabeceras `X-App-Name` y `X-API-Version`.

**Explicación:** En la pestaña `Headers` de Insomnia se puede ver las cabeceras de respuesta. Además de las cabeceras estándar (`server`, `content-type`, etc.), la API añade `X-App-Name: device_systems` y `X-API-Version: 1.0`. Estas cabeceras personalizadas permiten identificar la aplicación y su versión en cada comunicación cliente-servidor.

---

## Reflexión sobre el uso de FastAPI para construir APIs REST

Al desarrollar esta api

- **Validación automática:** Pydantic valida tipos, longitudes, emails y roles sin escribir código adicional. Los errores 422 son claros y específicos.
- **Documentación interactiva:** Swagger UI se genera solo con el código, permitiendo probar endpoints sin herramientas externas.
- **Parámetros de ruta y consulta:** FastAPI distingue automáticamente entre `{user_id}` y `?role=admin`, lo que simplifica el código.
- **Manejo de errores:** Con `HTTPException` se pueden devolver códigos 400, 404 y mensajes personalizados.
- **Cabeceras personalizadas:** Se añaden fácilmente con `response.headers`.

FastAPI hace que se acelere el desarrollo, reduce errores y produce APIs bien estructuradas y autodocumentadas. Es una excelente opción para proyectos backend modernos.


### Link Video Youtube

https://youtu.be/G8Z5m7-ULBk