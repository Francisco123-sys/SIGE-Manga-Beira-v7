import sqlite3
import os
from flask import g

DATABASE = 'database/sige.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        os.makedirs('database', exist_ok=True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_db(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def log_audit(user_id, operacao, detalhes, ip="127.0.0.1"):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO audit_logs (user_id, operacao, detalhes, ip_address)
        VALUES (?, ?, ?, ?)
    ''', (user_id, operacao, detalhes, ip))
    db.commit()