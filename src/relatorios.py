from fpdf import FPDF
from doencas import *

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch

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
        GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ') ') SEPARATOR ', ') AS sintomas 
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
        results = cursor.fetchone()
        
        if results:
            # Estilos para o Paragraph
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            
            # Cria um documento em modo paisagem
            pdf = SimpleDocTemplate("relatorio_doenca_reportlab.pdf", pagesize=landscape(letter))
            elements = []

            # Cabeçalhos da tabela
            headers = ['Doença', 'CID', 'Nomes Populares', 'Patógeno', 'Tipo do Patógeno', 'Sintomas e Taxa de Ocorrência']
            
            # Certifique-se de que cada campo em `results` não seja None
            data = [
                [Paragraph(results[0] if results[0] else "N/A", styleN), 
                 Paragraph(results[1] if results[1] else "N/A", styleN), 
                 Paragraph(results[2] if results[2] else "N/A", styleN), 
                 Paragraph(results[3] if results[3] else "N/A", styleN), 
                 Paragraph(results[4] if results[4] else "N/A", styleN), 
                 Paragraph(results[5] if results[5] else "N/A", styleN)]
            ]
            data_with_headers = [headers] + data

            # Ajuste de largura das colunas e altura das linhas
            col_widths = [1.5 * inch, 1 * inch, 1.5 * inch, 2 * inch, 1.5 * inch, 3 * inch]
            row_heights = [0.6 * inch] * len(data_with_headers)

            # Configura o estilo da tabela
            table = Table(data_with_headers, colWidths=col_widths, rowHeights=row_heights)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  # Cor de fundo do cabeçalho
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Cor do texto do cabeçalho
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centraliza o texto
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte do cabeçalho em negrito
                ('FONTSIZE', (0, 0), (-1, 0), 10),  # Tamanho da fonte do cabeçalho
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaçamento inferior do cabeçalho
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Cor de fundo das células
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grelha preta em toda a tabela
            ]))

            # Adiciona a tabela ao documento
            elements.append(table)

            # Build PDF
            pdf.build(elements)
            print("Relatório gerado com sucesso!")
        else:
            print("Doença não encontrada.")
    
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    
    finally:
        cursor.close()

    
#5 - Relatórios ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def relatorio_1(conn):
#     cursor = conn.cursor()
#     listar_doenca(conn)
#     opcao = int(input('Digite o id de uma doença para ser colocado no pdf:'))
    
#     sql = """
#     SELECT 
#         d.id, 
#         d.nome_tecnico, 
#         d.cid, 
#         dnp.nome_popular, 
#         p.nome_cientifico, 
#         p.tipo, 
#         GROUP_CONCAT(CONCAT(s.nome, ' (', ds.ocorrencia, ') ') SEPARATOR ', ') AS sintomas 
#     FROM doencas d 
#     JOIN patogenos p ON p.id = d.patogeno_id 
#     LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id 
#     JOIN doenca_sintoma ds ON d.id = ds.doenca_id 
#     JOIN sintomas s ON s.id = ds.sintoma_id 
#     WHERE d.id = %s
#     GROUP BY d.id, d.nome_tecnico, d.cid, dnp.nome_popular, p.nome_cientifico, p.tipo;
#     """
    
#     try:
#         cursor.execute(sql, (opcao,))
#         results = cursor.fetchone()
        
#         if results:
#             column_names = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas"]
            
#             # Início da geração do PDF
#             pdf = FPDF()
#             pdf.add_page()
#             pdf.set_font("Arial", size=12)
            
#             pdf.cell(200, 10, txt="Relatório de Doença Específica", ln=True, align='C')
#             pdf.ln(10)
            
#             for i, value in enumerate(results):
#                 if value is None:
#                     value = ""
#                 text = f"{column_names[i]}: {str(value).replace('’', "'").replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('…', '...')}"
#                 pdf.cell(200, 10, txt=text, ln=True, align='L')
            
#             pdf.output("relatorio_doenca_especifica.pdf")
#             print("Relatório gerado com sucesso!")
#         else:
#             print("Doença não encontrada.")
        
#         # Não é necessário chamar `fetchall()` após `fetchone()`

#     except mysql.connector.Error as err:
#         print(f"Erro: {err}")
    
#     finally:
#         cursor.close()


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
