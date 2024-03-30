import streamlit as st
from pymongo import MongoClient
from signup_page import signup_page
from forgot_password_page import forgot_password_page
from resolver_new import resolver_new
from resolver_form import resolver_form
from complaint_form import complaint_form
from resolver_home import resolver_home
from login_page import login_page
from admin_login_page import admin_login_page  # Add this import statement
from show_complaints import show_complaints  # Import the show_complaints function

# The rest of your code goes here...



# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]
complaint_collection = db["complaints"]
technician_collection = db["technicians"]

if __name__ == "__main__":
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if 'resolver_authenticated' not in st.session_state:
        st.session_state.resolver_authenticated = False

    page = st.sidebar.radio("Select an option", ["Admin", "Login", "Signup", "Forgot Password", "Resolver"])

    if st.session_state.authenticated:
        email = st.session_state.get('email', '')
        if email:
            complaint_form(email)
        else:
            st.error("Email not found in session. Please log in again.")
    elif st.session_state.resolver_authenticated:
        resolver_home()
    elif page == "Login":
        if login_page():
            st.session_state.authenticated = True
    elif page == "Signup":
        signup_page()
    elif page == "Forgot Password":
        forgot_password_page()
    elif page == "Resolver":
        if resolver_new():
            st.session_state.resolver_authenticated = True
    elif page == "Admin":
        if admin_login_page():
            st.session_state.authenticated = True
            show_complaints()
    else:
        st.warning("Please select an option from the sidebar.")
