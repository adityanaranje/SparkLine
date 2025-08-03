import sqlite3
import os
from datetime import datetime

class ActivityLogger:
    def __init__(self, db_path="db/activity.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_activity_table()

    def _create_activity_table(self):
        
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS activity (
                    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username TEXT NOT NULL,
                    DateTime TEXT NOT NULL,
                    Activities TEXT NOT NULL
                )
            ''')
            conn.commit()

    def log_activity(self, username: str, tab: str):
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO activity (Username, DateTime, Activities) VALUES (?, ?, ?)",
                (username, timestamp, tab)
            )
            conn.commit()

    def get_all_logs(self):
        
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM activity ORDER BY DateTime DESC")
            return cur.fetchall()

    def get_logs_by_user(self, username: str):
        
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT UserName, Activities, DateTime FROM activity WHERE Username = ? ORDER BY DateTime DESC", (username,))
            return cur.fetchall()
