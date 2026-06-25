import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado que:
    - Mide el tiempo de procesamiento de cada petición.
    - Agrega cabeceras X-Process-Time, X-App-Name, X-Request-ID.
    - Registra método, ruta y código de estado.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        start_time = time.time()
        method = request.method
        url = request.url.path
        
        response: Response = await call_next(request)
        
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"Method: {method} | Path: {url} | Status: {response.status_code} | "
            f"Time: {process_time:.4f}s | Request-ID: {request_id}"
        )
        
        return response