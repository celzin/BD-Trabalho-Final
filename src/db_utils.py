import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='avaliacao',
    charset="utf8mb4", # Win11
    collation="utf8mb4_general_ci" # Win11
)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='avaliacao',
        charset="utf8mb4",
        collation="utf8mb4_general_ci"
    )
    return conn

#CONSULTAS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def listar_patogenos(conn):
    cursor = conn.cursor()
    sql = "SELECT * FROM patogenos"
    cursor.execute(sql)
    results = cursor.fetchall()
    col_widths = [10, 30, 10]  #tamanho das colunas

    # Cabeçalhos
    headers = ["ID", "Nome Científico", "Tipo"]
    header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
    print(header_row)
    print("-" * (sum(col_widths) + len(col_widths) - 1))

    # Dados
    for row in results:
        print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
        
def listar_sintomas(conn):
    cursor = conn.cursor()
    sql = "SELECT * FROM sintomas"
    cursor.execute(sql)
    results = cursor.fetchall()
    col_widths = [10, 30]  #tamanho das colunas

    # Cabeçalhos
    headers = ["ID", "Nome"]
    header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
    print(header_row)
    print("-" * (sum(col_widths) + len(col_widths) - 1))

    # Dados
    for row in results:
        print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
        
def listar_nomes(conn):
    cursor = conn.cursor()
    sql = "SELECT * FROM doenca_nomes_populares"
    cursor.execute(sql)
    results = cursor.fetchall()
    col_widths = [10, 30]  #tamanho das colunas

    # Cabeçalhos
    headers = ["ID Doença", "Nome Popular"]
    header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
    print(header_row)
    print("-" * (sum(col_widths) + len(col_widths) - 1))

    # Dados
    for row in results:
        print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
