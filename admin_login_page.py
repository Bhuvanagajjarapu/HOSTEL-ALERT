import streamlit as st
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]

# Function for admin login page
def admin_login_page():
    st.title("Welcome to Admin Login Page")
    email = st.text_input("Enter your email", key="email_inputs")
    otp_sent = None

    if email.lower() == "22satyanaryanam31@gmail.com":
        if st.button("Send OTP", key='send_otp_btn'):
            user_data = login_collection.find_one({"email": email})
            if user_data:
                otp_sent = send_otp(email)
                if otp_sent:
                    st.session_state['email'] = email
                    st.info("OTP has been sent to your email. Please check your inbox and enter the OTP below.")
                    st.session_state['otp_sent'] = otp_sent
                    st.session_state['otp_verified'] = False
            else:
                otp_sent = send_otp(email)
                if otp_sent:
                    st.session_state['email'] = email
                    st.info("OTP has been sent to your email. Please check your inbox and enter the OTP below.")
                    st.session_state['otp_sent'] = otp_sent
                    st.session_state['otp_verified'] = False
                    login_collection.insert_one({"email": email})
    else:
        st.error("Please enter valid ADMIN email and then press Enter")

    if "otp_verified" in st.session_state and not st.session_state.otp_verified:
        otp_entered = st.text_input("Enter OTP", key="otp_input")
        if st.button("Verify OTP", key="verify_otp_btn"):
            if 'otp_sent' in st.session_state:
                otp_sent = st.session_state['otp_sent']
                if otp_sent is not None and otp_entered.strip() == otp_sent:
                    st.session_state['otp_verified'] = True
                    return True
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("No OTP sent. Please click 'Send OTP' first.")

# Function to send OTP to user's email
def send_otp(email):
    try:
        otp = str(random.randint(1000, 9999))
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {otp}")
        msg['Subject'] = 'Login OTP'
        msg['From'] = 'gajjarapubhuvana@gmail.com'
        msg['To'] = email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('gajjarapubhuvana@gmail.com', 'uhgf gktr rcsn jwst')
            smtp.send_message(msg)
        logging.info(f"OTP sent to {email}")
        return otp
    except Exception as e:
        logging.error(f"Error sending OTP to {email}: {e}")
        return None
