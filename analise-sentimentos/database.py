import sqlite3

DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                sentimento TEXT NOT NULL,
                polaridade REAL NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def salvar_comentario(texto, sentimento, polaridade):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO comentarios (texto, sentimento, polaridade) VALUES (?, ?, ?)",
            (texto, sentimento, polaridade)
        )
        conn.commit()

def listar_historico():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT texto, sentimento, polaridade, data FROM comentarios ORDER BY id DESC LIMIT 10")
        return cursor.fetchall()