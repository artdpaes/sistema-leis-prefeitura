from app.config.database import get_connection

def gerar_proximo_numero():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(numero_lei) FROM leis")
    ultimo = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return 1 if ultimo is None else ultimo + 1

def salvar_lei(numero, titulo, descricao, data_lei):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leis (numero_lei, titulo, descricao, data_lei) VALUES (%s, %s, %s, %s)",
        (numero, titulo, descricao, data_lei)
    )
    conn.commit()
    cursor.close()
    conn.close()
