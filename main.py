# import streamlit as st
# from pymongo import MongoClient
# from signup_page import signup_page
# from HOSTEL-ALERT.forgot_password_page import forgot_password_page
# from resolver_new import resolver_new
# from resolver_form import resolver_form
# from complaint_form import complaint_form
# from resolver_home import resolver_home
# from login_page import login_page
# from admin_login_page import admin_login_page  
# from show_complaints import show_complaints  

# # MongoDB setup
# client = MongoClient("mongodb://localhost:27017/")
# db = client["project"]
# login_collection = db["details"]
# complaint_collection = db["complaints"]
# technician_collection = db["technicians"]

# # Initialize session state variables
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if "resolver_authenticated" not in st.session_state:
#     st.session_state.resolver_authenticated = False

# if "email" not in st.session_state:
#     st.session_state.email = None  # Ensure email exists in session

# # Sidebar menu
# page = st.sidebar.radio("Select an option", ["Admin", "Login", "Signup", "Forgot Password", "Resolver"])

# if st.session_state.authenticated:
#     email = st.session_state.email  # Get email from session
#     if email:
#         st.write(f"Logged in as: {email}")  # Debugging info
#         complaint_form(email)
#     else:
#         st.error("Email not found in session. Please log in again.")
# elif st.session_state.resolver_authenticated:
#     resolver_home()
# elif page == "Login":
#     if login_page():
#         st.session_state.authenticated = True
# elif page == "Signup":
#     signup_page()
# elif page == "Forgot Password":
#     forgot_password_page()
# elif page == "Resolver":
#     if resolver_new():
#         st.session_state.resolver_authenticated = True
# elif page == "Admin":
#     if admin_login_page():
#         st.session_state.authenticated = True
#         show_complaints()
# else:
#     st.warning("Please select an option from the sidebar.")
import streamlit as st
from pymongo import MongoClient
from signup_page import signup_page
from forgot_password_page import forgot_password_page
from resolver_new import resolver_new
from resolver_form import resolver_form
from complaint_form import complaint_form
from resolver_home import resolver_home
from login_page import login_page
from admin_login_page import admin_login_page
from show_complaints import show_complaints

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]
complaint_collection = db["complaints"]
technician_collection = db["technicians"]

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False  # For students

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False  # For admin

if "resolver_authenticated" not in st.session_state:
    st.session_state.resolver_authenticated = False

if "email" not in st.session_state:
    st.session_state.email = None

# Sidebar menu
if st.session_state.authenticated:
    # Student successfully logged in -> Show complaint form
    complaint_form(st.session_state.email)

elif st.session_state.admin_authenticated:
    # Admin successfully logged in -> Show complaints
    show_complaints()

elif st.session_state.resolver_authenticated:
    # Resolver successfully logged in -> Show resolver dashboard
    resolver_home()

else:
    # Show menu options if no one is logged in
    page = st.sidebar.radio("Select an option", ["Admin", "Login", "Signup", "Forgot Password", "Resolver"])

    if page == "Login":
        if login_page():  # If student login is successful
            st.session_state.authenticated = True  # Set student login flag

    elif page == "Signup":
        signup_page()

    elif page == "Forgot Password":
        forgot_password_page()

    elif page == "Resolver":
        if resolver_new():
            st.session_state.resolver_authenticated = True  # Resolver login flag

    elif page == "Admin":
        if admin_login_page():  # If admin login is successful
            st.session_state.admin_authenticated = True  # Set admin login flag

    else:
        st.warning("Please select an option from the sidebar.")