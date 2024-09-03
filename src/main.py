from db_utils import *
from doencas import *
from diagnostico import * 
from relatorios import *

def main():
    conn = get_db_connection()

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
            cadastrar_doenca(conn)
        elif opcao == 2:
            listar_doenca(conn)
        elif opcao == 3:
            pesquisar_doenca(conn)
        elif opcao == 4:
            diagnostico(conn)
        elif opcao == 5:
            relatorios(conn)
        elif opcao == 6:
            print('Em Construção!')
        elif opcao == 7:
            print("Saindo...")
            break
        else:
            print("Opção inválida. Escolha um valor entre 1 e 7.")
    
    conn.close()

if __name__ == "__main__":
    main()

# import os
# from fpdf import FPDF

# #------------------------------------------------------------------EXECUÇÃO-------------------------------------------------------------------------------------------------------------------------------
# while True:
#     print()
#     print("--------------------------------MENU----------------------------------------")
#     print()
#     print("1 - Cadastrar doença.")
#     print("2 - Listar doenças.")
#     print("3 - Pesquisar doenças.")
#     print("4 - Diagnóstico.")
#     print("5 - Relatório.")
#     print("6 - Logs.")
#     print("7 - Sair.")
#     print()
#     opcao = int(input("Escolha uma opção: "))
#     if opcao == 1:
#         cadastrar_doenca()
#     elif opcao == 2:
#         listar_doenca()
#     elif opcao == 3:
#         pesquisar_doenca()
#     elif opcao == 4:
#         diagnostico()
#     elif opcao == 5:
#         relatorios()
#     elif opcao == 6:
#         print('Em Construção!')
#     elif opcao == 7:
#         print("7 - Sair.")
#         break
#     else:
#         print("Opção inválida. Escolha um valor entre 1 e 7.")
    
    
    