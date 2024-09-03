from db_utils import *

#4 - Diagnóstico ------------------------------------------------------------------------------------------------------------------------
def diagnostico(conn):
    cursor = conn.cursor()

    sintomas_input = input("Digite os sintomas separados por vírgula: ")
    sintomas_lista = [s.strip() for s in sintomas_input.split(',')]
    total_sintomas = len(sintomas_lista)
    
    placeholders = ', '.join(['%s'] * total_sintomas)
    sql = f"""
    SELECT 
        d.id, 
        d.nome_tecnico, 
        d.cid, 
        GROUP_CONCAT(DISTINCT dnp.nome_popular SEPARATOR ', ') AS nomes_populares, 
        p.nome_cientifico, 
        p.tipo, 
        GROUP_CONCAT(DISTINCT CONCAT(s.nome, ' (', ds.ocorrencia, ')') SEPARATOR ', ') AS sintomas,
        COUNT(DISTINCT s.id) AS matching_sintomas
    FROM doencas d 
    JOIN patogenos p ON p.id = d.patogeno_id 
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
    JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
    JOIN sintomas s ON s.id = ds.sintoma_id 
    WHERE s.nome IN ({placeholders}) 
    GROUP BY d.id, d.nome_tecnico, d.cid, p.nome_cientifico, p.tipo 
    HAVING matching_sintomas = %s
    ORDER BY matching_sintomas DESC, d.nome_tecnico;
    """
    
    try:
        cursor.execute(sql, tuple(sintomas_lista) + (total_sintomas,))
        results = cursor.fetchall()
        
        if not results:
            print("Nenhuma doença encontrada com os sintomas fornecidos.")
        else:
            print()
            print("Você pode estar com algumas das doenças abaixo:")
            print()
            col_widths = [10, 30, 10, 30, 30, 30, 100]  # Tamanho das colunas

            # Cabeçalhos
            headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Patógeno", "Tipo Patógeno", "Sintomas"]
            header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
            print(header_row)
            print("-" * (sum(col_widths) + len(col_widths) - 1))

            # Dados
            for row in results:
                print("".join(f"{str(cell):<{width}} " for cell, width in zip(row[:-1], col_widths)))  # Ignora a última coluna de contagem
                
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()