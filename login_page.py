import streamlit as st
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage
from complaint_form import complaint_form

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]

# Function to authenticate user based on email and OTP
def authenticate_user(email, otp_entered):
    user_data = login_collection.find_one({"email": email, "otp": otp_entered})
    return user_data is not None

# Function to send OTP to user's email
def send_otp(email):
    otp = str(random.randint(1000, 9999))
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Login OTP'
    msg['From'] = 'gajjarapubhuvana@gmail.com'  # Update with your email address
    msg['To'] = email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('gajjarapubhuvana@gmail.com', 'uhgf gktr rcsn jwst')  # Update with your email credentials
        smtp.send_message(msg)
    return otp

# Function for login page
def login_page():
    st.title("Login Page")
    email = st.text_input("Enter your email")
    otp_sent = None

    if st.button("Send OTP"):
        user_data = login_collection.find_one({"email": email})
        if user_data:
            otp_sent = send_otp(email)
            if otp_sent:
                st.session_state['email'] = email
                st.info("OTP has been sent to your email. Please check your inbox and enter the OTP below.")
                st.session_state['otp_sent'] = otp_sent  # Store the sent OTP in session state
                st.session_state['otp_verified'] = False

    if "otp_verified" in st.session_state and not st.session_state.otp_verified:
        otp_entered = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            if 'otp_sent' in st.session_state:  # Check if OTP has been sent
                otp_sent = st.session_state['otp_sent']  # Retrieve the sent OTP from session state
                if otp_sent is not None and otp_entered.strip() == otp_sent:
                    st.session_state['otp_verified'] = True
                    return True
                else:
                    st.error("Invalid OTP. Please try again.")
            else:
                st.error("No OTP sent. Please click 'Send OTP' first.")

# Main function to run the application
def main():
    if "authenticated" not in st.session_state:
        if login_page():
            st.session_state.authenticated = True
            st.rerun()
            st.success("Login Successful! Redirecting to complaints page...")
            email = st.session_state.get('email', '')
            if email:
                complaint_form(email)  # Call the complaint_form() function here after verifying OTP
            else:
                st.error("Email not found in session. Please log in again.")
    else:
        st.success("Login Successful!")
        email = st.session_state.get('email', '')
        if email:
            complaint_form(email)
        else:
            st.error("Email not found in session.")


if __name__ == "__main__":
    main()
