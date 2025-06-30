import sqlite3

con = sqlite3.connect('C:/ProjetoMVP/gee_dashboard_v1/gee_data.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT rowid, * FROM instalacao")
dados = cur.fetchall()
print(f"Total de registros: {len(dados)}")
