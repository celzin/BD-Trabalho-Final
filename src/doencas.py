from db_utils import *
# from db_utils import listar_patogenos, listar_sintomas, listar_nomes

#1 - Cadastrar doença --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def cadastrar_doenca(conn):
    cursor = conn.cursor()
    
    try:
        # Entrada dos dados da doença
        opcao = input("Quer adicionar uma nova doença? (s/n): ")
        if opcao.lower() == 's':
            nome_tecnico = input("Digite o nome técnico da doença: ")
            cid = input("Digite o CID da doença: ")

            # Adicionar patógeno
            print("-------------------------------------------------------------------------------PATÓGENOS-------------------------------------------------------------------------------------")
            listar_patogenos(conn)
            opcao = input("Quer adicionar um novo patógeno? (s/n): ")
            patogeno_id = None
            if opcao.lower() == 's':
                nome_cientifico = input("Digite o nome científico do patógeno: ")
                tipo = input("Digite o tipo do patógeno: ")
                sql = "INSERT INTO patogenos (nome_cientifico, tipo) VALUES (%s, %s)"
                cursor.execute(sql, (nome_cientifico, tipo))
                conn.commit()  # Confirma a inserção do patógeno
                patogeno_id = cursor.lastrowid
            else:
                patogeno_id = int(input("Digite o ID do patógeno: "))

            # Inserção na tabela 'doencas'
            sql_doenca = "INSERT INTO doencas (nome_tecnico, cid, patogeno_id) VALUES (%s, %s, %s)"
            cursor.execute(sql_doenca, (nome_tecnico, cid, patogeno_id))
            conn.commit()  # Confirma a inserção da doença
            print("Doença cadastrada com sucesso!")
            print()
        

        # Adicionar sintoma
        print("-------------------------------------------------------------------------------SINTOMAS-------------------------------------------------------------------------------------")
        listar_sintomas(conn)
        opcao = input("Quer adicionar um novo sintoma? (s/n): ")
        if opcao.lower() == 's':
            nome_sintoma = input("Digite o nome do sintoma: ")
            sql = "INSERT INTO sintomas (nome) VALUES (%s)"
            cursor.execute(sql, (nome_sintoma,))
            conn.commit()  # Confirma a inserção do sintoma
            print("Sintoma cadastrado com sucesso!")
            print()
        
        # Adicionar relação doença-sintoma
        print("-------------------------------------------------------------------------------DOENÇA SINTOMAS-------------------------------------------------------------------------------------")
        listar_doenca(conn)
        opcao = input("Quer adicionar um novo sintoma à doença? (s/n): ")
        if opcao.lower() == 's':
            doenca_id = int(input("Digite o ID da doença: "))
            listar_sintomas(conn)
            sintoma_id = int(input("Digite o ID do sintoma: "))
            ocorrencia = input("Digite a ocorrência do sintoma na doença: ")
            sql = "INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES (%s, %s, %s)"
            cursor.execute(sql, (doenca_id, sintoma_id, ocorrencia))
            conn.commit()  # Confirma a inserção da relação doença-sintoma
            print("Relação Doença x Sintoma cadastrado com sucesso!")
            print()

        # Adicionar relação doença-sintoma
        print("-------------------------------------------------------------------------------NOMES POPULARES-------------------------------------------------------------------------------------")
        listar_nomes(conn)
        opcao = input("Quer adicionar um novo nome popular à doença? (s/n): ")
        if opcao.lower() == 's':
            listar_doenca(conn)
            doenca_id = int(input("Digite o ID da doença: "))
            nome_popular = input("Digite o nome popular da doença: ")
            sql = "INSERT INTO doenca_nomes_populares (doenca_id, nome_popular) VALUES (%s, %s)"
            cursor.execute(sql, (doenca_id, nome_popular))
            conn.commit()  # Confirma a inserção da relação doença-sintoma
            print("Nome Popular cadastrado com sucesso!")
            print()
        
        print("-------------------------------------------------------------------------------DOENÇAS-------------------------------------------------------------------------------------")
        listar_doenca(conn)

        print("Operação Finalizada!")
        print()

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()  # Reverte a transação em caso de erro

    finally:
        cursor.close()

#2 - Listar doenças -------------------------------------------------------------------------------------------------------------------
def listar_doenca(conn):
    cursor = conn.cursor()
    sql = """
    SELECT 
        d.id,
        d.nome_tecnico,
        d.cid, 
        GROUP_CONCAT(DISTINCT dnp.nome_popular ORDER BY dnp.nome_popular SEPARATOR ', ') AS nomes_populares,
        p.nome_cientifico,
        p.tipo,
        GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ') ') SEPARATOR ', ') AS sintomas 
    FROM doencas d 
    JOIN patogenos p ON p.id = d.patogeno_id 
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
    LEFT JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
    LEFT JOIN sintomas s ON s.id = ds.sintoma_id 
    GROUP BY d.id, d.nome_tecnico, d.cid, p.nome_cientifico, p.tipo;"""

    cursor.execute(sql)
    results = cursor.fetchall()

    if not results:
        print("Nenhuma Doença cadastrada.")
    else:
        col_widths = [10, 30, 10, 30, 30, 30, 100]  #tamanho das colunas

        # Cabeçalhos
        headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Patógeno", "Tipo Patógeno", "Sintomas"]
        header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
        print(header_row)
        print("-" * (sum(col_widths) + len(col_widths) - 1))

        # Dados
        for row in results:
            print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
    return None

#3 - Pesquisar doenças -----------------------------------------------------------------------------------------------------------------------
def pesquisar_doenca(conn):
    cursor = conn.cursor()
    nome_tecnico = input("Digite o nome da doença: ")
    sql = """
    SELECT 
        d.id, 
        d.nome_tecnico, 
        d.cid, 
        dnp.nome_popular, 
        p.nome_cientifico, 
        p.tipo, 
        GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ') ') SEPARATOR ', ') AS sintomas 
    FROM doencas d 
    JOIN patogenos p ON p.id = d.patogeno_id 
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
    JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
    JOIN sintomas s ON s.id = ds.sintoma_id 
    WHERE d.nome_tecnico LIKE %s 
    GROUP BY d.id, d.nome_tecnico, d.cid, dnp.nome_popular, p.nome_cientifico, p.tipo;
    """
    
    try:
        cursor.execute(sql, (f"%{nome_tecnico}%",))
        results = cursor.fetchall()  # Use fetchall() to get all results

        if not results:
            print("Nenhuma Doença cadastrada com esse nome.")
        else:
            col_widths = [10, 30, 10, 30, 30, 30, 100]  # tamanho das colunas

            # Cabeçalhos
            headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Patógeno", "Tipo Patógeno", "Sintomas"]
            header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
            print(header_row)
            print("-" * (sum(col_widths) + len(col_widths) - 1))

            # Dados
            for row in results:
                print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()