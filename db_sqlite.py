import sqlite3

def criar_conexao():
    conn = sqlite3.connect("banco.sqlite")
    return conn

def criar_tabelas():
    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado TEXT NOT NULL,
        pais TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def inserir_cidade(nome, estado, pais):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cidades (nome, estado, pais) VALUES (?, ?, ?)", (nome, estado, pais))
    conn.commit()
    conn.close()

def listar_cidades():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cidades")
    dados = cursor.fetchall()
    conn.close()
    return dados
