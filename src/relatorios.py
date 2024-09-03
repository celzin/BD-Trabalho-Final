from fpdf import FPDF
from doencas import *

#5 - Relatórios ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def relatorio_1(conn):
    cursor = conn.cursor()

    listar_doenca(conn)
    opcao = int(input('Digite o id de uma doença para ser colocado no pdf:'))
    
    sql = """
    SELECT 
        d.nome_tecnico, 
        d.cid, 
        GROUP_CONCAT(DISTINCT dnp.nome_popular ORDER BY dnp.nome_popular SEPARATOR ', ') AS nomes_populares,
        p.nome_cientifico, 
        p.tipo, 
        GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ')') SEPARATOR ', ') AS sintomas 
    FROM doencas d 
    JOIN patogenos p ON p.id = d.patogeno_id 
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
    JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
    JOIN sintomas s ON s.id = ds.sintoma_id 
    WHERE d.id = %s
    GROUP BY d.nome_tecnico, d.cid, p.nome_cientifico, p.tipo;
    """
    
    try:
        cursor.execute(sql, (opcao,))
        result = cursor.fetchone()
        
        if result:
            pdf = FPDF(orientation='L')
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Cabeçalhos
            headers = ['Doença', 'CID', 'Nomes Populares', 'Patógeno', 'Tipo do Patógeno', 'Sintomas e Taxa de Ocorrência']
            col_widths = [40, 30, 40, 50, 40, 60]

            # Cores para cabeçalhos
            pdf.set_fill_color(79, 129, 189)  # Azul similar ao da imagem
            pdf.set_text_color(255, 255, 255)  # Texto branco
            pdf.set_font("Arial", 'B', 10)  # Negrito
            
            # Escrever cabeçalhos
            for header, width in zip(headers, col_widths):
                pdf.cell(width, 10, header, 1, 0, 'C', fill=True)
            pdf.ln()

            # Resetar cores e texto normal para o corpo
            pdf.set_fill_color(255, 255, 255)  # Branco para o corpo
            pdf.set_text_color(0, 0, 0)  # Texto preto
            pdf.set_font("Arial", size=10)

            # Dados
            # pdf.cell(col_widths[0], 10, str(result[0]), 1)
            # pdf.cell(col_widths[1], 10, str(result[1]), 1)
            # pdf.cell(col_widths[2], 10, str(result[2]), 1)
            # pdf.cell(col_widths[3], 10, str(result[3]), 1)
            # pdf.cell(col_widths[4], 10, str(result[4]), 1)
            # pdf.multi_cell(col_widths[5], 10, str(result[5]), 1)

            # Capturar a altura da última coluna (sem desenhá-la)
            x_before = pdf.get_x()
            y_before = pdf.get_y()

            # Desenha a última coluna "virtualmente" para capturar a altura
            pdf.multi_cell(col_widths[5], 10, str(result[5]), 0)  # Sem bordas temporárias
            y_after = pdf.get_y()  # Captura a altura da última coluna

            # Calcula a altura da linha com base na última coluna
            row_height = y_after - y_before

            # Volta para a posição original para desenhar as colunas na ordem certa
            pdf.set_xy(x_before, y_before)

            # Desenhar as outras colunas com a altura da última coluna capturada
            pdf.cell(col_widths[0], row_height, str(result[0]), 1)  # Coluna "Doença"
            pdf.cell(col_widths[1], row_height, str(result[1]), 1)  # Coluna "CID"
            pdf.cell(col_widths[2], row_height, str(result[2]), 1)  # Coluna "Nomes Populares"
            pdf.cell(col_widths[3], row_height, str(result[3]), 1)  # Coluna "Patógeno"
            pdf.cell(col_widths[4], row_height, str(result[4]), 1)  # Coluna "Tipo do Patógeno"

            # Desenhar agora a última coluna com base na altura capturada
            pdf.multi_cell(col_widths[5], 10, str(result[5]), 1)

            # Depois de desenhar, vá para a próxima linha
            pdf.ln(row_height)

            pdf.output("relatorio_doenca_especifica_formatado.pdf")
            print("Relatório gerado com sucesso!")
        else:
            print("Doença não encontrada.")
    
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()


def relatorio_2(conn):
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


def relatorio_3(conn):
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



def relatorios(conn):
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
            relatorio_1(conn)
        elif opcao == 2:
            relatorio_2(conn)
        elif opcao == 3:
            relatorio_3(conn)
        elif opcao == 4:
            print("Saindo do menu de relatórios.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")
