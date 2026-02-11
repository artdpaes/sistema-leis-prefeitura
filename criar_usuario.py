from getpass import getpass

from app.config.database import get_connection
from app.services.auth_service import senha_forte
from werkzeug.security import generate_password_hash


def main():
    print("Criação de usuário para o sistema de leis")
    username = input("Usuário: ").strip()
    if not username:
        print("Usuário não pode ser vazio.")
        return

    print(
        "A senha deve ter no mínimo 8 caracteres, "
        "com letra maiúscula, letra minúscula, número e caractere especial."
    )

    senha = getpass("Senha: ")
    confirmar = getpass("Confirme a senha: ")

    if senha != confirmar:
        print("As senhas não conferem.")
        return

    if not senha_forte(senha):
        print("Senha fraca. Use uma senha com os requisitos informados.")
        return

    is_admin_input = input("Usuário administrador? (s/N): ").strip().lower()
    is_admin = is_admin_input == "s"

    password_hash = generate_password_hash(senha)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username, password_hash, is_admin) VALUES (%s, %s, %s)",
        (username, password_hash, is_admin),
    )
    conn.commit()
    cursor.close()
    conn.close()

    tipo = "administrador" if is_admin else "comum"
    print(f"Usuário '{username}' ({tipo}) criado com sucesso.")


if __name__ == "__main__":
    main()

