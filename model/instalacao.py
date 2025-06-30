from model.base import get_db_connection


def listar_instalacoes():
    try:
        conexao = get_db_connection()
        instalacoes = conexao.execute(
            'SELECT rowid, * FROM instalacao').fetchall()
        conexao.close()
        return instalacoes
    except Exception as e:
        print(f"[ERRO listar_instalacoes] {e}")
        return []


def buscar_instalacao(id):
    conexao = get_db_connection()
    instalacao = conexao.execute(
        'SELECT rowid, * FROM instalacao WHERE rowid = ?', (id,)).fetchone()
    conexao.close()
    return instalacao


def cadastrar_instalacao(data):
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO instalacao (
                Ano, Bacia, Instalacao, Operador, Campo, 
                Emissoes_Escopo1, Emissoes_Escopo2, Emissoes_Total,
                Emissoes_CH4, Emissoes_CO2, Producao_Anual_Liquida, Intensidade_Emissoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['Ano'], data['Bacia'], data['Instalacao'], data['Operador'], data['Campo'],
            float(data['Emissoes_Escopo1']), float(
                data['Emissoes_Escopo2']), float(data['Emissoes_Total']),
            float(data['Emissoes_CH4']), float(data['Emissoes_CO2']), float(
                data['Producao_Anual_Liquida']), float(data['Intensidade_Emissoes'])
        ))
        conexao.commit()
        conexao.close()
        return "Instalação cadastrada com sucesso"
    except Exception as e:
        print(f"[ERRO cadastrar_instalacao] {e}", flush=True)
        return {"message": f"Erro ao cadastrar: {str(e)}"}


def deletar_instalacao(id):
    conexao = get_db_connection()
    conexao.execute('DELETE FROM instalacao WHERE rowid = ?', (id,))
    conexao.commit()
    conexao.close()
