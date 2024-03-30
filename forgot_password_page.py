import streamlit as st
from pymongo import MongoClient
from twilio.rest import Client

client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
detail = db["details"]

def set_new_password(email, new_password):
    
    detail.update_one({"email": email}, {"$set": {"password": new_password}})

def forgot_password_page():
    st.title("Forgot Password Page")
    email = st.text_input("Enter your email:")
    
    new_password = st.text_input("Enter your new password:", type="password")
    confirm_password = st.text_input("Confirm your new password:", type="password")

    if st.button("Reset Password"):
       
        if new_password == confirm_password:
           
            user = detail.find_one({"email": email})

            if user:
                
                set_new_password(email, new_password)

               
                st.success("Password successfully reset!")

            else:
                st.warning("Invalid email address")
        else:
            st.warning("Passwords do not match")


if __name__ == "__main__":
    forgot_password_page()
