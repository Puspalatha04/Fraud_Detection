
import streamlit as st

# Import the reset_user_password function from utils.py
from utils import reset_user_password

st.set_page_config(page_title="Reset Password", layout="centered")

st.title("🔒 Reset Your Password")
st.markdown("Enter your username and a new password to reset your account credentials.")

with st.form("password_reset_form"):
    username_to_reset = st.text_input("Username", key="reset_username")
    new_password_1 = st.text_input("New Password", type="password", key="new_password_1")
    new_password_2 = st.text_input("Confirm New Password", type="password", key="new_password_2")

    reset_button = st.form_submit_button("Reset Password")

    if reset_button:
        if not username_to_reset or not new_password_1 or not new_password_2:
            st.error("All fields are required.")
        elif new_password_1 != new_password_2:
            st.error("New password and confirmation do not match.")
        else:
            if reset_user_password(username_to_reset, new_password_1):
                st.success("Your password has been successfully reset. You can now log in with your new password.")
            # Error message is handled within reset_user_password function
