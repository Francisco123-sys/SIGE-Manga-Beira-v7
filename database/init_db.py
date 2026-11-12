import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'database/sige.db'

def init_db():
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    # Migração segura para bases de dados existentes
    cursor.execute("PRAGMA table_info(grades)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    for col, col_type in [
        ('faltas_justificadas', 'INTEGER DEFAULT 0'),
        ('faltas_nao_justificadas', 'INTEGER DEFAULT 0'),
        ('total_faltas', 'INTEGER DEFAULT 0'),
        ('comentario_professor', "TEXT DEFAULT ''")
    ]:
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE grades ADD COLUMN {col} {col_type}")

    cursor.execute("PRAGMA table_info(turmas)")
    turma_cols = [row[1] for row in cursor.fetchall()]
    if 'sala' not in turma_cols:
        cursor.execute("ALTER TABLE turmas ADD COLUMN sala TEXT DEFAULT 'Sala 01'")
        
    cursor.execute("INSERT OR IGNORE INTO academic_years (id, ano, ativo) VALUES (1, 2026, 1)")
    
    for c in range(1, 13):
        nivel = 'Primário' if c <= 6 else 'Secundário'
        cursor.execute("INSERT OR IGNORE INTO classes (id, numero, nivel) VALUES (?, ?, ?)", (c, c, nivel))
        
    disciplinas = [
        ('Português', 'POR'), ('Inglês', 'ING'), ('História', 'HIS'),
        ('Geografia', 'GEO'), ('Biologia', 'BIO'), ('Física', 'FIS'),
        ('Matemática', 'MAT'), ('Química', 'QUI'), ('Educação Visual', 'EDV'),
        ('Agro-pecuária', 'AGP'), ('Educação Física', 'EDF')
    ]
    for disc, cod in disciplinas:
        cursor.execute("INSERT OR IGNORE INTO subjects (nome, codigo) VALUES (?, ?)", (disc, cod))

    cursor.execute("SELECT id FROM users WHERE role = 'admin'")
    if not cursor.fetchone():
        pwd_hash = generate_password_hash("AdminSIGE2026!")
        cursor.execute('''
            INSERT INTO users (code, nome, email, password_hash, role, contacto)
            VALUES ('ADM-000001', 'Administrador Geral', 'admin@sige.co.mz', ?, 'admin', '840000000')
        ''', (pwd_hash,))
        
    profiles = [
        ('SEC-000001', 'Maria Catarina Carlos Penicela', 'secretaria@sige.co.mz', 'chefe_secretaria', 'Secretaria123!'),
        ('DIR-000001', 'Director Escolar', 'director@sige.co.mz', 'director', 'Director123!'),
        ('PED1-000001', 'Director Pedagógico 1º Ciclo', 'pedagogico1@sige.co.mz', 'pedagogico_1', 'Pedagogico123!'),
        ('PED2-000001', 'Director Pedagógico 2º Ciclo', 'pedagogico2@sige.co.mz', 'pedagogico_2', 'Pedagogico123!'),
        ('PROF-000001', 'Professor Silva', 'professor@sige.co.mz', 'teacher', 'Professor123!')
    ]
    for code, nome, email, role, pwd in profiles:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (code, nome, email, password_hash, role, contacto)
                VALUES (?, ?, ?, ?, ?, '841234567')
            ''', (code, nome, email, generate_password_hash(pwd), role))

    conn.commit()
    conn.close()
    print("Base de dados SIGE inicializada com sucesso!")

if __name__ == '__main__':
    init_db()
