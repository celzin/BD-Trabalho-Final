# pip install mysql-connector-python
# pip install tabulate 
# pip install fpdf

import os
from fpdf import FPDF
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='avaliacao',
    charset="utf8mb4", # Win11
    collation="utf8mb4_general_ci" # Win11
)
#CONSULTAS-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def listar_patogenos():
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
        
def listar_sintomas():
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
        
def listar_nomes():
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

#1 - Cadastrar doença --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def cadastrar_doenca():
    cursor = conn.cursor()
    
    try:
        # Entrada dos dados da doença
        opcao = input("Quer adicionar uma nova doença? (s/n): ")
        if opcao.lower() == 's':
            nome_tecnico = input("Digite o nome técnico da doença: ")
            cid = input("Digite o CID da doença: ")

            # Adicionar patógeno
            print("-------------------------------------------------------------------------------PATÓGENOS-------------------------------------------------------------------------------------")
            listar_patogenos()
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
        listar_sintomas()
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
        listar_doenca()
        opcao = input("Quer adicionar um novo sintoma à doença? (s/n): ")
        if opcao.lower() == 's':
            doenca_id = int(input("Digite o ID da doença: "))
            listar_sintomas()
            sintoma_id = int(input("Digite o ID do sintoma: "))
            ocorrencia = input("Digite a ocorrência do sintoma na doença: ")
            sql = "INSERT INTO doenca_sintoma (doenca_id, sintoma_id, ocorrencia) VALUES (%s, %s, %s)"
            cursor.execute(sql, (doenca_id, sintoma_id, ocorrencia))
            conn.commit()  # Confirma a inserção da relação doença-sintoma
            print("Relação Doença x Sintoma cadastrado com sucesso!")
            print()

        # Adicionar relação doença-sintoma
        print("-------------------------------------------------------------------------------NOMES POPULARES-------------------------------------------------------------------------------------")
        listar_nomes()
        opcao = input("Quer adicionar um novo nome popular à doença? (s/n): ")
        if opcao.lower() == 's':
            listar_doenca()
            doenca_id = int(input("Digite o ID da doença: "))
            nome_popular = input("Digite o nome popular da doença: ")
            sql = "INSERT INTO doenca_nomes_populares (doenca_id, nome_popular) VALUES (%s, %s)"
            cursor.execute(sql, (doenca_id, nome_popular))
            conn.commit()  # Confirma a inserção da relação doença-sintoma
            print("Nome Popular cadastrado com sucesso!")
            print()
        
        print("-------------------------------------------------------------------------------DOENÇAS-------------------------------------------------------------------------------------")
        listar_doenca()

        print("Operação Finalizada!")
        print()

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        conn.rollback()  # Reverte a transação em caso de erro

    finally:
        cursor.close()

#2 - Listar doenças -------------------------------------------------------------------------------------------------------------------
def listar_doenca():
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
def pesquisar_doenca():
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

#4 - Diagnóstico ------------------------------------------------------------------------------------------------------------------------
def diagnostico():
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

#5 - Relatórios ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def relatorio_1():
    cursor = conn.cursor()
    listar_doenca()
    opcao = int(input('Digite o id de uma doença para ser colocado no pdf:'))
    
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
    WHERE d.id = %s
    GROUP BY d.id, d.nome_tecnico, d.cid, dnp.nome_popular, p.nome_cientifico, p.tipo;
    """
    
    try:
        cursor.execute(sql, (opcao,))
        results = cursor.fetchone()
        
        if results:
            column_names = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas"]
            
            # Início da geração do PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.cell(200, 10, txt="Relatório de Doença Específica", ln=True, align='C')
            pdf.ln(10)
            
            for i, value in enumerate(results):
                if value is None:
                    value = ""
                text = f"{column_names[i]}: {str(value).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('…', '...')}"
                pdf.cell(200, 10, txt=text, ln=True, align='L')
            
            pdf.output("relatorio_doenca_especifica.pdf")
            print("Relatório gerado com sucesso!")
        else:
            print("Doença não encontrada.")
        
        # Não é necessário chamar `fetchall()` após `fetchone()`

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()


def relatorio_2():
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
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            # Definição dos nomes das colunas
            column_names = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas"]
            
            # Início da geração do PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            
            pdf.cell(200, 10, txt="Relatório de Todas as Doenças", ln=True, align='C')
            pdf.ln(10)
            
            for row in results:
                for i, value in enumerate(row):
                    if value is None:
                        value = ""
                    text = f"{column_names[i]}: {str(value).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('…', '...')}"
                    pdf.cell(200, 10, txt=text, ln=True, align='L')
                pdf.ln(10)
            
            pdf.output("relatorio_todas_doencas.pdf")
            print("Relatório gerado com sucesso!")
        else:
            print("Nenhuma doença encontrada.")
    
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()


def relatorio_3():
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
        GROUP_CONCAT(DISTINCT dnp.nome_popular ORDER BY dnp.nome_popular SEPARATOR ', ') AS nomes_populares, 
        p.nome_cientifico, 
        p.tipo, 
        GROUP_CONCAT(DISTINCT CONCAT(s.nome, ' (', ds.ocorrencia, ')') SEPARATOR ', ') AS sintomas,
        COUNT(DISTINCT s.id) AS sintomas_qtd
    FROM doencas d 
    JOIN patogenos p ON p.id = d.patogeno_id 
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
    JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
    JOIN sintomas s ON s.id = ds.sintoma_id 
    WHERE s.nome IN ({placeholders}) 
    GROUP BY d.id, d.nome_tecnico, d.cid, p.nome_cientifico, p.tipo 
    HAVING sintomas_qtd = %s
    ORDER BY sintomas_qtd DESC, d.nome_tecnico;
    """
    
    try:
        cursor.execute(sql, tuple(sintomas_lista) + (total_sintomas,))
        results = cursor.fetchall()
        
        if not results:
            print("Nenhuma doença encontrada com os sintomas fornecidos.")
        else:
            # Definição dos nomes das colunas
            column_names = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas", "Quantidade de Sintomas"]
            
            # Início da geração do PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.cell(200, 10, txt="Relatório de Doenças Baseadas em Sintomas", ln=True, align='C')
            pdf.ln(10)

            for row in results:
                for i, value in enumerate(row):
                    if value is None:
                        value = ""
                    if i < len(column_names):
                        text = f"{column_names[i]}: {str(value).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('…', '...')}"
                    else:
                        text = f"Coluna {i + 1}: {str(value).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('…', '...')}"
                    pdf.cell(200, 10, txt=text, ln=True, align='L')
                pdf.ln(10)
            
            pdf.output("relatorio_doencas_sintomas.pdf")
            print("Relatório gerado com sucesso!")
    
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()



def relatorios():
    while True:
        print()
        print("--------------------------------MENU RELATÓRIOS----------------------------------------")
        print()
        print("1 - Relatório de uma doença")
        print("2 - Relatório para listar todas doenças")
        print("3 - Relatório de doenças mais prováveis por sintomas")
        print("4 - Sair.")
        print()
        
        opcao = int(input("Escolha uma opção: "))
        if opcao == 1:
            relatorio_1()
        elif opcao == 2:
            relatorio_2()
        elif opcao == 3:
            relatorio_3()
        elif opcao == 4:
            print("Saindo do menu de relatórios.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

#------------------------------------------------------------------EXECUÇÃO-------------------------------------------------------------------------------------------------------------------------------
while True:
    print()
    print("--------------------------------MENU----------------------------------------")
    print()
    print("1 - Cadastrar doença.")
    print("2 - Listar doenças.")
    print("3 - Pesquisar doenças.")
    print("4 - Diagnóstico.")
    print("5 - Relatório.")
    print("6 - Logs.")
    print("7 - Sair.")
    print()
    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        cadastrar_doenca()
    elif opcao == 2:
        listar_doenca()
    elif opcao == 3:
        pesquisar_doenca()
    elif opcao == 4:
        diagnostico()
    elif opcao == 5:
        relatorios()
    elif opcao == 6:
        print('Em Construção!')
    elif opcao == 7:
        print("7 - Sair.")
        break
    else:
        print("Opção inválida. Escolha um valor entre 1 e 7.")
    
    
    