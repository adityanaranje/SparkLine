import sqlite3
import time
from argon2 import PasswordHasher, exceptions
import os
import streamlit as st



class Auth:
    def __init__(self, db_path="db/users.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_users_table()
        self.ph = PasswordHasher()
        self.logged_user = ""


    def _create_users_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_user(self, username, password):
        if len(password) < 8:
            st.toast("Password must be at least 8 characters long",icon="⚠️")
            return False

        password_hash = self.ph.hash(password)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
                conn.commit()
                st.toast("User registered successfully",icon="🎉")
                self.logged_user = username
                return True
        except sqlite3.IntegrityError:
            st.toast("Username already exists",icon="🚫")
            return False

    def validate_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE username = ?", (username,))
            row = cur.fetchone()

        if row:
            stored_hash = row[0]
            try:
                if self.ph.verify(stored_hash, password):
                    st.toast("Login successful",icon="✅" )
                    self.logged_user = username
                    return True
            except exceptions.VerifyMismatchError:
                st.toast("Incorrect credentials",icon="🚫")
                return False
        else:
            st.toast("Username not found",icon="⚠️")
            return False
        
    def get_logged_user(self):
        return self.logged_user