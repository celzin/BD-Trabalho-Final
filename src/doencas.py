from db_utils import *
from logs import *
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

            cursor.execute("SELECT COUNT(*) FROM doencas WHERE cid = %s", (cid,))
            cid_existe = cursor.fetchone()[0]
            if cid_existe > 0:
                print(f"Erro: Já existe uma doença cadastrada com o CID '{cid}'.")
                return  

            # Adicionar patógeno
            print("-------------------------------------------------------------------------------PATÓGENOS-------------------------------------------------------------------------------------")
            listar_patogenos(conn)
            opcao = input("Quer adicionar um novo patógeno? (s/n): ")
            patogeno_id = None
            if opcao.lower() == 's':
                nome_cientifico = input("Digite o nome científico do patógeno: ")

                tipos_patogenos = ["Bactéria", "Vírus", "Fungo", "Parasita", "Protozoário"] #, "Príon", "Helminto", "Riquétsia"
                print("Selecione o tipo de patógeno:")
                for idx, tipo in enumerate(tipos_patogenos, 1):
                    print(f"{idx} - {tipo}")
                tipo_opcao = int(input("Escolha o número correspondente ao tipo de patógeno: "))
                if 1 <= tipo_opcao <= len(tipos_patogenos):
                    tipo_selecionado = tipos_patogenos[tipo_opcao - 1]
                else:
                    print("Opção inválida. Cadastro de patógeno cancelado.")
                    return
                
                sql = "INSERT INTO patogenos (nome_cientifico, tipo) VALUES (%s, %s)"
                cursor.execute(sql, (nome_cientifico, tipo_selecionado))
                conn.commit() 
                patogeno_id = cursor.lastrowid
            else:
                patogeno_id = int(input("Digite o ID do patógeno: "))

            # Inserção na tabela 'doencas'
            sql_doenca = "INSERT INTO doencas (nome_tecnico, cid, patogeno_id) VALUES (%s, %s, %s)"
            cursor.execute(sql_doenca, (nome_tecnico, cid, patogeno_id))
            conn.commit()
            
            registrar_log(f"Cadastro de Doença: {nome_tecnico}, CID: {cid}, Patógeno ID: {patogeno_id}",)
            print("Doença cadastrada com sucesso!")
            print()
        

        # Adicionar sintoma
        print("-------------------------------------------------------------------------------SINTOMAS-------------------------------------------------------------------------------------")
        listar_sintomas(conn)
        opcao = input("Quer adicionar um novo sintoma? (s/n): ")
        if opcao.lower() == 's':
            nome_sintoma = input("Digite o nome do sintoma: ")

            # Verificar se o sintoma já existe
            cursor.execute("SELECT COUNT(*) FROM sintomas WHERE nome = %s", (nome_sintoma,))
            sintoma_existe = cursor.fetchone()[0]
            if sintoma_existe > 0:
                print(f"Erro: O sintoma '{nome_sintoma}' já está cadastrado.")
                return  

            sql = "INSERT INTO sintomas (nome) VALUES (%s)"
            cursor.execute(sql, (nome_sintoma,))
            conn.commit() 

            registrar_log(f"Cadastro de sintoma: {nome_tecnico}")
            print("Sintoma cadastrado com sucesso!")
            print()
        
        # Adicionar relação doença-sintoma
        print("-------------------------------------------------------------------------------DOENÇA SINTOMAS-------------------------------------------------------------------------------------")
        listar_doenca(conn)
        opcao = input("Quer adicionar um novo sintoma à doença? (s/n): ")
        if opcao.lower() == 's':
            doenca_id = int(input("Digite o ID da doença: "))

            cursor.execute("SELECT COUNT(*) FROM doencas WHERE id = %s", (doenca_id,))
            doenca_existe = cursor.fetchone()[0]
            if doenca_existe == 0:
                print(f"Erro: Nenhuma doença cadastrada com o ID '{doenca_id}'.")
                return 
        
            listar_sintomas(conn)
            sintoma_id = int(input("Digite o ID do sintoma: "))

            cursor.execute("SELECT COUNT(*) FROM sintomas WHERE id = %s", (sintoma_id,))
            sintoma_existe = cursor.fetchone()[0]
            if sintoma_existe == 0:
                print(f"Erro: Nenhum sintoma cadastrado com o ID '{sintoma_id}'.")
                return 

            # Menu para selecionar o nível de ocorrência
            niveis_ocorrencia = ["muito comum", "comum", "pouco comum", "raro", "muito raro"]
            print("Selecione o nível de ocorrência do sintoma:")
            for idx, nivel in enumerate(niveis_ocorrencia, 1):
                print(f"{idx} - {nivel}")
            nivel_opcao = int(input("Escolha o número correspondente ao nível de ocorrência: "))
            if 1 <= nivel_opcao <= len(niveis_ocorrencia):
                nivel_selecionado = niveis_ocorrencia[nivel_opcao - 1]
            else:
                print("Opção inválida. Associação do sintoma cancelada.")
                return

            sql = "INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES (%s, %s, %s)"
            cursor.execute(sql, (doenca_id, sintoma_id, nivel_selecionado))
            conn.commit() 

            registrar_log(f"Cadastro de sintoma: {sintoma_id} à doença: {doenca_id}")
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
            conn.commit()  

            registrar_log(f"Cadastro de nome popular: {nome_popular} à doença: {doenca_id}")
            print("Nome Popular cadastrado com sucesso!")
            print()
        
        print("-------------------------------------------------------------------------------DOENÇAS-------------------------------------------------------------------------------------")
        listar_doenca(conn)

        print("Operação Finalizada!")
        print()

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()  

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
        col_widths = [10, 30, 10, 30, 30, 30, 100]  

        registrar_log("Consulta realizada: Listagem de todas as doenças")

        headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Patógeno", "Tipo Patógeno", "Sintomas"]
        header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
        print(header_row)
        print("-" * (sum(col_widths) + len(col_widths) - 1))

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
        results = cursor.fetchall() 

        if not results:
            print("Nenhuma Doença cadastrada com esse nome.")
        else:
            col_widths = [10, 30, 10, 30, 30, 30, 100] 

            registrar_log(f"Consulta realizada: Pesquisa de doença: {nome_tecnico}")

            headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Patógeno", "Tipo Patógeno", "Sintomas"]
            header_row = "".join(f"{header:<{width}} " for header, width in zip(headers, col_widths))
            print(header_row)
            print("-" * (sum(col_widths) + len(col_widths) - 1))

            for row in results:
                print("".join(f"{str(cell):<{width}} " for cell, width in zip(row, col_widths)))
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()