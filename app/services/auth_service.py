from typing import Optional, Dict, Any

import re
from werkzeug.security import check_password_hash, generate_password_hash

from app.config.database import get_connection


def senha_forte(senha: str) -> bool:
    """
    Mesma regra usada no script criar_usuario.py:
    - mínimo 8 caracteres
    - ao menos 1 letra maiúscula
    - ao menos 1 letra minúscula
    - ao menos 1 dígito
    - ao menos 1 caractere especial
    """
    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[a-z]", senha):
        return False
    if not re.search(r"[0-9]", senha):
        return False
    if not re.search(r"[^A-Za-z0-9]", senha):
        return False
    return True


def buscar_usuario_por_username(username: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, is_admin FROM usuarios WHERE username = %s",
        (username,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "password_hash": row[2],
        "is_admin": row[3],
    }


def autenticar_usuario(username: str, senha: str) -> Optional[Dict[str, Any]]:
    usuario = buscar_usuario_por_username(username)
    if not usuario:
        return None

    if not check_password_hash(usuario["password_hash"], senha):
        return None

    return usuario


def criar_usuario(
    username: str, senha: str, is_admin: bool = False
) -> tuple[bool, str]:
    """
    Cria um usuário novo.
    Retorna (ok, mensagem).
    """
    if not username:
        return False, "Usuário não pode ser vazio."

    if not senha_forte(senha):
        return (
            False,
            "Senha fraca. Use ao menos 8 caracteres, com maiúsculas, minúsculas, número e caractere especial.",
        )

    password_hash = generate_password_hash(senha)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash, is_admin) VALUES (%s, %s, %s)",
            (username, password_hash, is_admin),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        cursor.close()
        conn.close()
        return False, "Não foi possível criar o usuário (talvez username já exista)."

    cursor.close()
    conn.close()
    return True, "Usuário criado com sucesso."

