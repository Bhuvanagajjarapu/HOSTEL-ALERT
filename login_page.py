

import streamlit as st
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]

# Function to authenticate user
def authenticate_user(username, password):
    user_data = login_collection.find_one({"username": username, "password": password})
    return user_data  # Return full user document instead of True/False

def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_data = authenticate_user(username, password)
        if user_data:
            st.session_state.authenticated = True
            st.session_state.email = user_data.get("email")  # Store email in session
            st.rerun()  # Refresh app to reflect login state
        else:
            st.error("Invalid username or password. Please try again.")

    return st.session_state.authenticated  # Return authentication status
