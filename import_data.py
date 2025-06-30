import sqlite3
import pandas as pd
import os


# Caminho para os arquivos CSV
caminho_base = r'C:\ProjetoMVP\Dados projeto MVP'
arquivo_instalacao = os.path.join(caminho_base, 'tabela_por_instalacao.csv')
arquivo_campo = os.path.join(caminho_base, 'tabela_por_campo.csv')

# Verificando arquivos visíveis na pasta
print('\n arquivos que o python está vendo na pasta:')
if os.path.isdir(caminho_base):
    arquivos = os.listdir(caminho_base)
    for f in arquivos:
        print(' -', f)

    # Verificações manuais com os nomes exatos
    print('\n comparações manuais:')
    print('arquivo_instalacao está na lista?',
          'tabela_por_instalacao.csv' in arquivos)
    print('arquivo_campo está na lista?', 'tabela_por_campo.csv' in arquivos)
else:
    print('caminho base não existe!')

print('\n verificação final com os.path.isfile:')
print('arquivo de instalação existe?', os.path.isfile(arquivo_instalacao))
print('arquivo de campo existe?', os.path.isfile(arquivo_campo))


# Nome do banco de dados SQLite
db_name = 'gee_data.db'


# Criação da conexão com o SQLite
conexao = sqlite3.connect(db_name)
cursor = conexao.cursor()

# -------------------------------------------------
# Criação da TABELA por instalação
# -------------------------------------------------
cursor.execute('''
               CREATE TABLE IF NOT EXISTS instalacao (
               Ano TEXT,
               Bacia TEXT,
               Instalacao TEXT,
               Operador TEXT,
               Campo TEXT,
               Emissoes_Escopo1 REAL,
               Emissoes_Escopo2 REAL,
               Emissoes_Total REAL,
               Emissoes_CH4 REAL,
               Emissoes_CO2 REAL,
               Producao_Anual_Liquida REAL,
               Intensidade_Emissoes REAL
    )
''')

# -------------------------------------------------
# Criação da TABELA por campo
# -------------------------------------------------
cursor.execute('''
               CREATE TABLE IF NOT EXISTS campo (
               Ano TEXT,
               Bacia TEXT,
               Campo TEXT,
               Operador TEXT,
               Emissoes_Escopo1 REAL,
               Emissoes_Escopo2 REAL,
               Emissoes_CH4 REAL,
               Emissoes_CO2 REAL,
               Emissoes_GEE REAL,
               Producao_Anual_Liquida REAL,
               Intensidade_Emissoes REAL
    )
''')

# -------------------------------------------------
# Leitura e inserção dos dados
# -------------------------------------------------

# Função para limpar e converter colunas numéricas (substitui vírgula por ponto)


def limpar_numeros(df):
    for coluna in df.select_dtypes(include=['object']):
        df[coluna] = df[coluna].str.replace(',', '.', regex=False)
    return df


# Mapeamento de nomes do CSV -> nomes usados no banco
mapeamento_colunas = {
    'Instalação': 'Instalacao',
    'Emissões  Escopo 1  (tCO₂eq)': 'Emissoes_Escopo1',
    'Emissões Escopo 2 (tCO₂eq)': 'Emissoes_Escopo2',
    'Total de emissões (kgCO₂eq)': 'Emissoes_Total',
    'Emissões CH₄ (t)': 'Emissoes_CH4',
    'Emissões CO₂ (t)': 'Emissoes_CO2',
    'Produção Anual Líquida (Boe)': 'Producao_Anual_Liquida',
    'Intensidade de Emissões (kgCO₂eq/boe)': 'Intensidade_Emissoes'
}


# --- INSTALAÇÂO ---
try:
    print(f'Lendo: {arquivo_instalacao}')
    df_instalacao = pd.read_csv(
        arquivo_instalacao, sep=',', encoding='utf-8', skipinitialspace=True)
    df_instalacao.rename(columns=mapeamento_colunas, inplace=True)
    df_instalacao = limpar_numeros(df_instalacao)
    df_instalacao.to_sql('instalacao', conexao,
                         if_exists='replace', index=False)
    print('Dados da tabela por instalação importados com sucesso!')
except Exception as e:
    print('Erro ao importar dados da tabela por instalação:', e)


# --- CAMPO ---
try:
    print(f'lendo: {arquivo_campo}')
    df_campo = pd.read_csv(arquivo_campo, sep=',',
                           encoding='utf-8', skipinitialspace=True)
    df_campo = limpar_numeros(df_campo)
    df_campo.to_sql('campo', conexao, if_exists='replace', index=False)
    print('Dados da tabela por campo importados com sucesso!')
except Exception as e:
    print('Erro ao importar dados da tabela por campo:', e)

# Verificar quantos registros foram inseridos na tabela instalacao
cursor = sqlite3.connect(db_name).cursor()
try:
    cursor.execute('SELECT COUNT(*) FROM instalacao')
    total = cursor.fetchone()[0]
    print(f'\n✅ Total de registros na tabela instalacao: {total}')
except Exception as e:
    print('Erro ao contar registros na tabela instalacao:', e)

# ----------------------------------------
# Finaliza conexão
# ----------------------------------------
conexao.commit()
conexao.close()

print('Dados importados com sucesso para banco gee_data.db.')
