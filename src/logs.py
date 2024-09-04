import logging
from datetime import datetime

# Configuração básica de logging
LOG_FILE = 'operacoes.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Função para registrar operações
def registrar_log(mensagem):
    logging.info(mensagem)

# Função para registrar logs de erro
def registrar_erro(mensagem):
    logging.error(mensagem)

# Função para gerar o relatório de logs
def gerar_relatorio_de_logs():
    log_file = 'operacoes.log'
    relatorio_file = 'relatorio_logs.txt'

    try:
        # Abrindo o arquivo de logs
        with open(log_file, 'r') as log:
            conteudo = log.readlines()

        # Criando o relatório de logs em formato .txt
        with open(relatorio_file, 'w') as relatorio:
            relatorio.write("Relatório de Operações Registradas\n")
            relatorio.write("=" * 40 + "\n\n")
            for linha in conteudo:
                relatorio.write(linha)
        
        print(f"Relatório gerado com sucesso em: {relatorio_file}")
        registrar_log("Relatório de logs gerado.")
    
    except FileNotFoundError:
        print("Arquivo de logs não encontrado.")
        registrar_log("Erro ao gerar relatório de logs: arquivo não encontrado.")