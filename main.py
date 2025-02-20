import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
from signup_page import signup_page
from forgot_password_page import forgot_password_page
from resolver_new import resolver_new
from resolver_home import resolver_home
from login_page import login_page
from admin_login_page import admin_login_page
from show_complaints import get_mongo_query, get_complaints, prompt  
from complaint_form import complaint_form

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key missing. Check your .env file.")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]
complaint_collection = db["complaints"]
technician_collection = db["technicians"]

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "resolver_authenticated" not in st.session_state:
    st.session_state.resolver_authenticated = False

if "email" not in st.session_state:
    st.session_state.email = None

if "page" not in st.session_state:
    st.session_state.page = "Admin"

if "landing_page_viewed" not in st.session_state:
    st.session_state.landing_page_viewed = False

# Welcome Page (Only shows once)
if not st.session_state.landing_page_viewed:
    st.markdown("""
        <style>
            .main { text-align: center; }
            h1 { color: #004aad; font-size: 3rem; }
            p { font-size: 1.2rem; color: #333; }
            .button { padding: 15px 20px; font-size: 1rem; color: white; background: #004aad; 
                      border: none; border-radius: 5px; cursor: pointer; text-decoration: none; }
            .button:hover { background: #00358a; }
        </style>
        <div class="main">
            <h1>Welcome to Hostel Alert</h1>
            <p>Your one-stop solution for lodging complaints and getting quick resolutions.</p>
        </div>
        """, unsafe_allow_html=True
    )

    if st.button("Proceed to Dashboard"):
        st.session_state.landing_page_viewed = True
        st.rerun()

    st.stop()

# Sidebar Navigation
if not (st.session_state.authenticated or st.session_state.admin_authenticated or st.session_state.resolver_authenticated):
    st.session_state.page = st.sidebar.radio("Select an option", ["Admin", "Login", "Signup", "Forgot Password", "Resolver"])

# **Navigation Logic**
if st.session_state.authenticated:
    complaint_form(st.session_state.email)  # Show student complaint form

elif st.session_state.admin_authenticated:
    st.title("Admin Dashboard - Complaints")
    
    question = st.text_input("Ask a query about complaints:", key="input")
    submit = st.button("Get Complaints")

    if submit and question:
        query = get_mongo_query(question, prompt)
        complaints = get_complaints(query)
        
        if complaints:
            st.subheader("Complaints List")
            for complaint in complaints:
                st.write(f"- **Student Name:** {complaint['student_name']}, **Student ID:** {complaint['student_id']}, "
                         f"**Hostel:** {complaint['hostel']}, **Room Number:** {complaint['room_number']}, "
                         f"**Complaint:** {complaint['complaint']}, **Department:** {complaint['department']}")
        else:
            st.info("No complaints found for the given query.")

elif st.session_state.resolver_authenticated:
    resolver_home()  # Show resolver home page

else:
    if st.session_state.page == "Login":
        if login_page():
            st.session_state.authenticated = True
            st.rerun()

    elif st.session_state.page == "Signup":
        signup_page()

    elif st.session_state.page == "Forgot Password":
        forgot_password_page()

    elif st.session_state.page == "Resolver":
        if resolver_new():
            st.session_state.resolver_authenticated = True
            st.rerun()

    elif st.session_state.page == "Admin":
        if admin_login_page():
            st.session_state.admin_authenticated = True
            st.rerun()
