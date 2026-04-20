import sqlite3
import pandas as pd
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "data/transactions.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                timestamp TEXT,
                transaction_type TEXT,
                transaction_amount REAL,
                account_balance REAL,
                is_anomaly INTEGER,
                anomaly_probability REAL,
                processed_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_account ON transactions(account_id)")
        conn.commit()

def save_transaction(tx, is_anomaly, proba, model_version):
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO transactions
            (transaction_id, account_id, timestamp, transaction_type,
             transaction_amount, account_balance, is_anomaly, anomaly_probability, processed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx.TransactionID, tx.AccountID, tx.Timestamp.isoformat(),
            tx.TransactionType, tx.TransactionAmount, tx.AccountBalance,
            int(is_anomaly), proba, datetime.now().isoformat()
        ))
        conn.commit()

def get_account_history(account_id, limit=10):
    with get_db() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT ?",
            conn, params=[account_id, limit]
        )
    return df
