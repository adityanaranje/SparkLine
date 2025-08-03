import streamlit as st
import re

class LoginPage:
    def __init__(self, authenticate):
        self.authenticate = authenticate
        self.logged_user_name = ""

    def is_valid_username(self, username):
        if len(username) < 6:
            return False
        if not re.fullmatch(r'[a-zA-Z0-9]+', username):
            return False
        letter_count = sum(1 for c in username if c.isalpha())
        return letter_count >= 3

    def login_user(self):
        sidebar = st.sidebar

        is_valid_user = None
        with sidebar:
            auth_option = st.radio("Choose Option", ["Register","Login"], horizontal=True)

            if auth_option == 'Login':
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")

                if st.button("Login"):
                    is_valid_user =  self.authenticate.validate_user(login_username, login_password)

            if auth_option == "Register":
                register_username = st.text_input("Username", key="reg_user")
                register_password = st.text_input("Password", type="password", key="reg_pass")

                if st.button("Register"):
                    if self.is_valid_username(register_username):
                        is_valid_user =  self.authenticate.add_user(register_username, register_password)
                    else:
                        st.toast("Username must be at least 6 characters long, contain only letters and numbers, and include at least 3 letters.",icon="❌")
                        
                    
        return is_valid_user, self.authenticate.get_logged_user()