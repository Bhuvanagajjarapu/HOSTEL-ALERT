import streamlit as st
from pymongo import MongoClient
import random
import smtplib
from email.message import EmailMessage
from complaint_form import complaint_form  # Import the complaint_form function from complaint_form.py

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]

# Function to authenticate user based on email and OTP
def authenticate_user(email, otp_entered):
    user_data = login_collection.find_one({"email": email, "otp": otp_entered})
    return user_data is not None

# Function to send OTP to user's email
# def send_otp(email):
#     otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP
#     # Send OTP via email
#     msg = EmailMessage()
#     msg.set_content(f"Your OTP is: {otp}")
#     msg['Subject'] = 'Login OTP'
#     msg['From'] = 'gajjarapubhuvana@gmail.com'  # Update with your email address
#     msg['To'] = email
#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:  # Update with your SMTP server details
#             smtp.starttls()  # Add this line for TLS encryption
#             smtp.login('gajjarapubhuvana@gmail.com', 'uhgf gktr rcsn jwst')  # Update with your email credentials
#             smtp.send_message(msg)
#         return otp
#     except Exception as e:
#         st.error(f"Error sending OTP: {e}")
#         return None
def send_otp(email):
    otp = str(random.randint(1000, 9999))
    st.session_state['otp_sent'] = otp  # Store OTP in session
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Login OTP'
    msg['From'] = 'gajjarapubhuvana@gmail.com'
    msg['To'] = email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('gajjarapubhuvana@gmail.com', 'uhgf gktr rcsn jwst')
        smtp.send_message(msg)
    return otp


# Function to login page
def login_page():
    st.title("Login Page")
    email = st.text_input("Enter your email")

    if st.button("Send OTP"):
        user_data = login_collection.find_one({"email": email})
        if user_data:
            otp_sent = send_otp(email)
            if otp_sent:
                st.session_state['email'] = email  # Save email to session state
                st.info("OTP has been sent to your email. Please check your inbox and enter the OTP below.")
                otp_entered = st.text_input("Enter OTP")
                if st.button("Verify OTP"):
                    if otp_entered == otp_sent:
                        st.success("OTP Verified! Redirecting to complaints page...")
                        return True
                    else:
                        st.error("Invalid OTP. Please try again.")
        else:
            st.error("Email not found. Please enter a valid email.")
    return False

# Function to display link page
def link_page():
    st.title("Link Page")
    st.write("This is the link page.")
    # You can add any content or links here

# Main function to run the application
def main():
    if "authenticated" not in st.session_state:
        if login_page():
            st.session_state.authenticated = True
            st.experimental_rerun()
            st.success("Login Successful!")
            complaint_form()  # Call the complaint_form() function here after verifying OTP
    else:
        st.success("Login Successful!")
        complaint_form()

    # After successful login and complaint submission, show link page
    if "authenticated" in st.session_state and complaint_form.submitted:
        link_page()

if __name__ == "__main__":
    main()
