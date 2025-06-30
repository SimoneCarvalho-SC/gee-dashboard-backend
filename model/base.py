import sqlite3
import os


def get_db_connection():

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.abspath(os.path.join(
        basedir, '..', 'database', 'gee_data.db'))

    conexao = sqlite3.connect(db_path)
    conexao.row_factory = sqlite3.Row
    return conexao
