import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'operacoes.log')

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a'  # Modo de append, para que os logs não sejam sobrescritos
)

def registrar_log(mensagem):
    logging.info(mensagem)

def registrar_erro(mensagem):
    logging.error(mensagem)

def gerar_relatorio_de_logs():
    try:
        # print(f"O caminho do arquivo de log é: {LOG_FILE}")
        
        with open(LOG_FILE, 'r') as log:
            conteudo = log.readlines()

        if conteudo:
            print("--------------------------------LOG----------------------------------------")
            for linha in conteudo:
                print(linha.strip())
        else:
            print("O arquivo de log está vazio.")

        registrar_log("Logs exibidos no terminal.")
    
    except FileNotFoundError:
        print(f"Arquivo de logs não encontrado: {LOG_FILE}")
        registrar_log("Erro ao exibir logs: arquivo não encontrado.")
