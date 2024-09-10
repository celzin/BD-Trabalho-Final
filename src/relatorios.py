from fpdf import FPDF
from doencas import *
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch

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
                [Paragraph(results[0] if results[0] else "", styleN), 
                 Paragraph(results[1] if results[1] else "", styleN), 
                 Paragraph(results[2] if results[2] else "", styleN), 
                 Paragraph(results[3] if results[3] else "", styleN), 
                 Paragraph(results[4] if results[4] else "", styleN), 
                 Paragraph(results[5] if results[5] else "", styleN)]
            ]
            data_with_headers = [headers] + data

            # Ajuste de largura das colunas e altura das linhas
            col_widths = [1.5 * inch, 1 * inch, 1.5 * inch, 2 * inch, 1.5 * inch, 3 * inch]
            row_heights = [0.6 * inch] * len(data_with_headers)

            # Configura o estilo da tabela
            table = Table(data_with_headers, colWidths=col_widths, rowHeights=row_heights)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
                ('FONTSIZE', (0, 0), (-1, 0), 10),  
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DAE1F3')),  
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BEC9DC')),  
            ]))
            
            elements.append(table)
            pdf.build(elements)

            registrar_log(f"Relatório gerado para a doença com ID {opcao}")
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
            # Estilos para o Paragraph
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            
            # Criação do PDF
            pdf = SimpleDocTemplate("relatorio_todas_doencas_reportlab.pdf", pagesize=landscape(letter))
            elements = []

            # Cabeçalhos da tabela
            headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas"]
            
            # Preparar os dados para a tabela, convertendo cada campo para `Paragraph`
            data = []
            for row in results:
                data.append([
                    Paragraph(str(row[0] if row[0] else ""), styleN),
                    Paragraph(str(row[1] if row[1] else ""), styleN),
                    Paragraph(str(row[2] if row[2] else ""), styleN),
                    Paragraph(str(row[3] if row[3] else ""), styleN),
                    Paragraph(str(row[4] if row[4] else ""), styleN),
                    Paragraph(str(row[5] if row[5] else ""), styleN),
                    Paragraph(str(row[6] if row[6] else ""), styleN),
                ])
            
            # Inclui os cabeçalhos e os dados na tabela
            data_with_headers = [headers] + data

            # Ajuste de largura das colunas
            col_widths = [0.8 * inch, 1.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch, 1 * inch, 2.5 * inch]

            # Configura o estilo da tabela com alternância de cores
            table = Table(data_with_headers, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
                ('FONTSIZE', (0, 0), (-1, 0), 10),  
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DAE1F3')),  
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BEC9DC')),  
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#DAE1F3'), colors.white]),  
            ]))

            elements.append(table)
            pdf.build(elements)

            registrar_log(f"Relatório de TODAS DOENÇAS gerado ")
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
        GROUP_CONCAT(DISTINCT CONCAT(s.nome, ' (', ds.ocorrencia, ') ') ORDER BY s.nome SEPARATOR ', ') AS todos_sintomas
    FROM doencas d
    JOIN patogenos p ON p.id = d.patogeno_id
    LEFT JOIN doenca_nomes_populares dnp ON dnp.doenca_id = d.id
    JOIN doenca_sintoma ds ON ds.doenca_id = d.id
    JOIN sintomas s ON s.id = ds.sintoma_id
    WHERE d.id IN (
        SELECT d.id
        FROM doencas d
        JOIN doenca_sintoma ds ON ds.doenca_id = d.id
        JOIN sintomas s ON s.id = ds.sintoma_id
        WHERE s.nome IN ({placeholders})
        GROUP BY d.id
        HAVING COUNT(DISTINCT s.id) >= %s
    )
    GROUP BY d.id, d.nome_tecnico, d.cid, p.nome_cientifico, p.tipo
    ORDER BY d.nome_tecnico;
    """
    
    try:
        cursor.execute(sql, tuple(sintomas_lista) + (total_sintomas,))
        results = cursor.fetchall()
        
        if not results:
            print("Nenhuma doença encontrada com os sintomas fornecidos.")
        else:
            # Estilos para o Paragraph
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            
            # Início da geração do PDF
            pdf = SimpleDocTemplate("relatorio_doencas_sintomas_reportlab.pdf", pagesize=landscape(letter))
            elements = []

            # Cabeçalhos da tabela
            # headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas", "Quantidade de Sintomas"]
            headers = ["ID", "Nome Técnico", "CID", "Nomes Populares", "Nome Científico", "Tipo", "Sintomas", ]
            
            # Preparar os dados para a tabela, convertendo cada campo para `Paragraph`
            data = []
            for row in results:
                data.append([
                    Paragraph(str(row[0] if row[0] is not None else ""), styleN),
                    Paragraph(str(row[1] if row[1] is not None else ""), styleN),
                    Paragraph(str(row[2] if row[2] is not None else ""), styleN),
                    Paragraph(str(row[3] if row[3] is not None else ""), styleN),
                    Paragraph(str(row[4] if row[4] is not None else ""), styleN),
                    Paragraph(str(row[5] if row[5] is not None else ""), styleN),
                    Paragraph(str(row[6] if row[6] is not None else ""), styleN),
                    # Paragraph(str(row[7] if row[7] is not None else ""), styleN)
                ])
            
            # Inclui os cabeçalhos e os dados na tabela
            data_with_headers = [headers] + data

            # Ajuste de largura das colunas
            col_widths = [0.8 * inch, 1.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch, 1 * inch, 2.5 * inch, 1 * inch]

            # Configura o estilo da tabela
            table = Table(data_with_headers, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  
                ('FONTSIZE', (0, 0), (-1, 0), 10), 
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12), 
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#DAE1F3')),  
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BEC9DC')),  
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#DAE1F3'), colors.white]),  
            ]))

            # Adiciona a tabela ao documento
            elements.append(table)
            pdf.build(elements)

            registrar_log(f"Relatório gerado para a doenças com sintomas: {sintomas_lista}")
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
