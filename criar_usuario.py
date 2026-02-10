from getpass import getpass

from werkzeug.security import generate_password_hash

from app.config.database import get_connection


def main():
    print("Criação de usuário para o sistema de leis")
    username = input("Usuário: ").strip()
    if not username:
        print("Usuário não pode ser vazio.")
        return

    senha = getpass("Senha: ")
    confirmar = getpass("Confirme a senha: ")

    if senha != confirmar:
        print("As senhas não conferem.")
        return

    password_hash = generate_password_hash(senha)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
        (username, password_hash),
    )
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Usuário '{username}' criado com sucesso.")


if __name__ == "__main__":
    main()

