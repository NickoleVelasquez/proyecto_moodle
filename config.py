import sqlite3

# Crear la base de datos con usuarios y roles
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insertar usuarios de ejemplo
def insert_example_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    c.execute("INSERT INTO users (username, password, role) VALUES ('user', 'user123', 'usuario')")
    conn.commit()
    conn.close()

init_db()
insert_example_users()

