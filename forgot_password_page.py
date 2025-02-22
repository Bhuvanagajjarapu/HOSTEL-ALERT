
import streamlit as st
import smtplib
import random
from email.message import EmailMessage
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
detail = db["details"]

# Email Credentials (Use App Passwords if 2FA is enabled)
# secret

# Function to send OTP via email
def send_otp(email):
    otp = str(random.randint(1000, 9999))  # Generate 4-digit OTP
    
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Password Reset OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login to email
            smtp.send_message(msg)  # Send OTP email
        return otp  # Return OTP for verification
    except Exception as e:
        st.error(f"Error sending OTP: {e}")
        return None

# Function to update password in MongoDB
def set_new_password(email, new_password):
    detail.update_one({"email": email}, {"$set": {"password": new_password}})
    st.success("Password successfully reset! Please log in with your new password.")

# Forgot Password Page
import streamlit as st
import smtplib
import random
from email.message import EmailMessage
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
detail = db["details"]

# Email Credentials (Use App Passwords if 2FA is enabled)
  # Use App Password instead of real password
#   secret

# Function to send OTP via email
def send_otp(email):
    otp = str(random.randint(1000, 9999))  # Generate 4-digit OTP
    
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Password Reset OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Secure the connection
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login to email
            smtp.send_message(msg)  # Send OTP email
        return otp  # Return OTP for verification
    except Exception as e:
        st.error(f"Error sending OTP: {e}")
        return None

# Function to update password in MongoDB
def set_new_password(email, new_password):
    detail.update_one({"email": email}, {"$set": {"password": new_password}})
    st.success("✅ Password successfully reset! Please log in with your new password.")

# Forgot Password Page
def forgot_password_page():
    st.title("🔒 Forgot Password")

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False  # Flag to track OTP sending
        st.session_state.otp_verified = False  # Flag to track OTP verification
        st.session_state.otp = None  # Store OTP for validation
        st.session_state.email = None  # Store user email

    # Step 1: Enter Email
    if not st.session_state.otp_sent:
        email = st.text_input("📧 Enter your email:")
        if st.button("Send OTP"):
            user = detail.find_one({"email": email})
            if user:
                otp = send_otp(email)
                if otp:
                    st.session_state.otp = otp  # Store OTP
                    st.session_state.email = email  # Store email
                    st.session_state.otp_sent = True
                    st.success("✅ OTP sent! Please check your email.")
            else:
                st.warning("⚠️ Email not found! Please check and try again.")

    # Step 2: Enter OTP (Only if OTP is sent)
    if st.session_state.otp_sent and not st.session_state.otp_verified:
        entered_otp = st.text_input("🔢 Enter the OTP sent to your email:")
        if st.button("Verify OTP"):
            if entered_otp == st.session_state.otp:
                st.session_state.otp_verified = True
                st.success("✅ OTP verified! You can now reset your password.")
            else:
                st.error("❌ Invalid OTP! Please try again.")

    # Step 3: Reset Password (Only if OTP is verified)
    if st.session_state.otp_verified:
        new_password = st.text_input("🔑 Enter your new password:", type="password")
        confirm_password = st.text_input("🔑 Confirm your new password:", type="password")

        if st.button("Reset Password"):
            if new_password == confirm_password:
                set_new_password(st.session_state.email, new_password)
                st.session_state.otp_sent = False  # Reset session state
                st.session_state.otp_verified = False
            else:
                st.warning("⚠️ Passwords do not match!")

# Run the function when the script is executed
if __name__ == "__main__":
    forgot_password_page()

