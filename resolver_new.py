import streamlit as st
from pymongo import MongoClient
from twilio.rest import Client
from resolver_home import resolver_home

ALLOWED_RESOLVER_NUMBERS = {
    "+918919542599": "ELECTRICIAN",
    "9550676575": "HOUSEKEEPER",
    "07382944698": "TECHSUPPORT",
    "7382904875": "PLUMBER",
    "9908268058": "AC REPAIR"
}

client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]
resolver_collection = db["resolvers"]
def resolver_new():
    st.title("Resolver Page")
    st.write("Enter your phone number to log in:")
    phone_number_key = "phone_number_input"
    phone_number = st.text_input("Phone Number", key=phone_number_key)

    if st.button("Click Here"):
       
        if phone_number in ALLOWED_RESOLVER_NUMBERS:
            resolver_type = ALLOWED_RESOLVER_NUMBERS[phone_number]
            st.session_state.resolver_authenticated = True
            st.session_state.resolver_phone_number = phone_number
            st.session_state.resolver_type = resolver_type

           
            st.success(f"Logged in as {resolver_type} with phone number {phone_number}")
            resolver_home()
    
            

            
            st.markdown(f"[Click here to go to Resolver Home](#resolver-home)", unsafe_allow_html=True)

        else:
            st.error("Invalid phone number. Please try again.")

if __name__ == "_main_":
    resolver_new()