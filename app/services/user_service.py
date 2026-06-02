from app.data.users_db import usuarios_db

def _get_next_id():
    if not usuarios_db:
        return 1
    return max(u["id"] for u in usuarios_db) + 1

def obtener_todos():
    return usuarios_db.copy()

def obtener_por_id(user_id: int):
    for u in usuarios_db:
        if u["id"] == user_id:
            return u
    return None

def obtener_por_email(email: str):
    for u in usuarios_db:
        if u["email"] == email:
            return u
    return None

def guardar_usuario(datos: dict):
    nuevo = datos.copy()
    nuevo["id"] = _get_next_id()
    usuarios_db.append(nuevo)
    return nuevo

def actualizar_usuario_completo(user_id: int, nuevos_datos: dict):
    usuario = obtener_por_id(user_id)
    if not usuario:
        return None
    usuario.clear()
    usuario.update(nuevos_datos)
    usuario["id"] = user_id
    return usuario

def actualizar_usuario_parcial(user_id: int, datos_parciales: dict):
    usuario = obtener_por_id(user_id)
    if not usuario:
        return None
    for key, value in datos_parciales.items():
        if key != "id":
            usuario[key] = value
    return usuario

def eliminar_usuario(user_id: int):
    usuario = obtener_por_id(user_id)
    if not usuario:
        return False
    usuarios_db.remove(usuario)
    return True