# # resolver_new.py
# import streamlit as st
# from pymongo import MongoClient
# import streamlit_extras.switch_page_button as switch_page

# # Allowed Resolver Numbers & Assigned Departments
# ALLOWED_RESOLVER_NUMBERS = {
#     "+918919542599": "ELECTRICIAN",
#     "9550676575": "HOUSEKEEPER",
#     "07382944698": "TECHSUPPORT",
#     "7382904875": "PLUMBER",
#     "9908268058": "AC REPAIR"
# }

# # MongoDB Connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["project"]
# complaint_collection = db["complaints"]

# def resolver_new():
#     st.title("Resolver Page 👨🏻‍🔧")
#     st.write("Enter your phone number to log in:")
    
#     phone_number = st.text_input("Phone Number")
    
#     if st.button("Login"):
#         if phone_number in ALLOWED_RESOLVER_NUMBERS:
#             st.session_state.resolver_authenticated = True
#             st.session_state.resolver_phone_number = phone_number
#             st.session_state.resolver_type = ALLOWED_RESOLVER_NUMBERS[phone_number]
#             st.success(f"Logged in as {st.session_state.resolver_type}")
            
#             # Redirect to resolver_home.py
#             switch_page.switch_page("resolver_home")
#         else:
#             st.error("Invalid phone number. Please try again.")

# if __name__ == "__main__":
#     resolver_new()
import streamlit as st

# Allowed Resolver Numbers & Assigned Departments
ALLOWED_RESOLVER_NUMBERS = {
    "+918919542599": "ELECTRICIAN",
    "9550676575": "HOUSEKEEPER",
    "07382944698": "TECHSUPPORT",
    "7382904875": "PLUMBER",
    "9908268058": "AC REPAIR"
}

def resolver_new():
    st.title("Resolver Login 👨🏻‍🔧")
    
    phone_number = st.text_input("Enter your phone number:")
    
    if st.button("Login"):
        if phone_number in ALLOWED_RESOLVER_NUMBERS:
            st.session_state.resolver_authenticated = True
            st.session_state.resolver_type = ALLOWED_RESOLVER_NUMBERS[phone_number]
            st.success(f"Logged in as {st.session_state.resolver_type}")
        else:
            st.error("Invalid phone number. Please try again.")

    return st.session_state.resolver_authenticated
