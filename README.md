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

| Dependencia | ¿Para qué sirve? (explicación sencilla) |
|---|---|
| FastAPI | Es el motor de la API. Proporciona todas las herramientas para crear los endpoints (rutas) y manejar las peticiones HTTP. |
| Uvicorn | Es el servidor que pone en marcha la API y la mantiene a la escucha de peticiones (como un recepcionista que atiende llamadas). |
| email-validator | Es una pequeña ayuda que permite verificar que los correos electrónicos tengan un formato válido (por ejemplo, que contengan un `@` y un dominio). |

Estas dependencias se instalan automáticamente con el siguiente comando:

```bash
python -m uv add fastapi uvicorn[standard] email-validator
```
---


