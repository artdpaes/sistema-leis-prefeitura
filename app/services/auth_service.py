from typing import Optional, Dict, Any

from werkzeug.security import check_password_hash

from app.config.database import get_connection


def buscar_usuario_por_username(username: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash FROM usuarios WHERE username = %s",
        (username,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None

    return {"id": row[0], "username": row[1], "password_hash": row[2]}


def autenticar_usuario(username: str, senha: str) -> Optional[Dict[str, Any]]:
    usuario = buscar_usuario_por_username(username)
    if not usuario:
        return None

    if not check_password_hash(usuario["password_hash"], senha):
        return None

    return usuario

