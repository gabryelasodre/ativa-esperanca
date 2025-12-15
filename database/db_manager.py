import sqlite3

# Define o nome do banco de dados (já usado no original)
DB_NAME = 'ativa_esperanca.db'

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Tabela USERS (já existe)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       email
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL,
                       role
                       TEXT
                       NOT
                       NULL
                       DEFAULT
                       'volunteer'
                   )
                   """)

    # Tabela STUDENTS (NOVA TABELA) - Para cadastro dos participantes
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS students
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       birth_date
                       TEXT,
                       enrollment_date
                       TEXT
                       NOT
                       NULL,
                       status
                       TEXT
                       NOT
                       NULL
                       DEFAULT
                       'Active'
                   )
                   """)

    # Tabela ACTIVITIES (já existe, mas precisa de uma tabela de PRESENÇAS)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS activities
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT
                       NOT
                       NULL,
                       description
                       TEXT,
                       date
                       TEXT,
                       volunteer_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       volunteer_id
                   ) REFERENCES users
                   (
                       id
                   )
                       )
                   """)

    # Tabela PRESENCE_RECORDS (NOVA TABELA) - Para registrar a presença dos alunos nas atividades
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS presence_records
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       student_id
                       INTEGER
                       NOT
                       NULL,
                       activity_id
                       INTEGER
                       NOT
                       NULL,
                       date
                       TEXT
                       NOT
                       NULL,
                       is_present
                       INTEGER
                       NOT
                       NULL
                       DEFAULT
                       1,
                       FOREIGN
                       KEY
                   (
                       student_id
                   ) REFERENCES students
                   (
                       id
                   ),
                       FOREIGN
                       KEY
                   (
                       activity_id
                   ) REFERENCES activities
                   (
                       id
                   )
                       )
                   """)

    conn.commit()
    conn.close()