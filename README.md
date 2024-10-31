<div align="center" style="display: inline_block">
  <img align="center" alt="VS" src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" />
  <img align="center" alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img align="center" alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="SQL" src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" /> 
  <img align="center" alt="MariaDB" src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white" /> 
</div>


<br>
<h1 align="center">
    <a>
        <img alt="Banner" title="#Banner" style="object-fit: fill; width: 961px, height:200px;" src="imgs/github-header-image.png"/>
    </a>
</h1>

## 🗂️ Estrutura do Repositório

- `imgs/`: Diretório com as imagens utilizadas no repositório.
- `src/`: Diretório com os scripts Python usados para gerar os percursos do agente e realizar as análises.
- `logs/`: Diretório com o registro de todas as ações realizadas.
- `reports/`: Diretório com os relatórios gerados.

## 📝 Resumo

<div align="justify">

Neste projeto, implementamos um sistema de apoio ao diagnóstico de doenças, conectado a um banco de dados relacional, que foi definido previamente. O objetivo do sistema é auxiliar profissionais de saúde a identificarem possíveis doenças com base nos sintomas informados, além de permitir o gerenciamento e consulta de doenças no catálogo.

1. **Cadastrar Doença**: Permite cadastrar novas doenças com informações detalhadas, como CID, nome técnico, nomes populares, patógeno, e sintomas.
2. **Listar Doenças**: O sistema possibilita listar todas as doenças cadastradas no sistema.
3. **Pesquisar Doenças**: O sistema possibilita pesquisar doenças específicas pelo nome.
4. **Diagnóstico**: O usuário pode inserir sintomas e obter uma lista das doenças mais prováveis, com base na ocorrência dos sintomas cadastrados para cada doença.
5. **Emissão de Relatórios**: O sistema é capaz de gerar relatórios sobre doenças específicas e também relatórios com base em sintomas. Esses relatórios podem ser exportados em formato PDF.
6. **Logs de Acesso e Operações**: Todas as operações realizadas no sistema são registradas em arquivos de log, incluindo a data e hora, para facilitar o rastreamento de ações.

</div>

## 🔄 Compilação e Execução 

### Pré-requisitos:
1. **Banco de Dados MySQL**: Certifique-se de que o MySQL esteja instalado e configurado. Você precisará criar um banco de dados conforme descrito nos scripts SQL fornecidos (`esquema.sql` e `dados.sql`).
2. **Python 3.x**: O projeto foi implementado em Python. Certifique-se de que o Python esteja instalado.
3. **Dependências**: Instale as bibliotecas necessárias, como `mysql-connector-python`, `FPDF`, e `reportlab`, utilizando o `pip`.
   
    ```bash
    pip install mysql-connector-python fpdf reportlab
    ```

### Configuração da Conexão com o Banco de Dados:
Abra o arquivo `db_utils.py` e configure os parâmetros de conexão para corresponder ao seu ambiente. Os parâmetros principais a serem ajustados são:

  ```python
  conn = mysql.connector.connect(
      host='localhost',      # Substitua pelo endereço do seu servidor MySQL
      user='root',           # Substitua pelo seu usuário MySQL
      password='root',       # Substitua pela senha do seu usuário MySQL
      database='avaliacao',  # O banco de dados utilizado
      charset="utf8mb4",     
      collation="utf8mb4_general_ci"
  )
  ```

  ```python
  def get_db_connection():
      conn = mysql.connector.connect(
          host='localhost',      # Substitua pelo endereço do seu servidor MySQL
          user='root',           # Substitua pelo seu usuário MySQL
          password='root',       # Substitua pela senha do seu usuário MySQL
          database='avaliacao',  # O banco de dados utilizado
          charset="utf8mb4",
          collation="utf8mb4_general_ci"
      )
      return conn
  ```

### Execução do Sistema:
1. Navegue até a pasta `src` onde o código está localizado.
2. Execute o arquivo `main.py` para iniciar a aplicação.
   ```bash
   python main.py
   ```

## 📞 Contato

<table align="center">
  <tr>
    <th>Participante</th>
    <th>Contato</th>
  </tr>
  <tr>
    <td>Celso</td>
    <td><a href="https://t.me/celso_vsf"><img align="center" height="20px" width="90px" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> </td>
  </tr>
</table>
