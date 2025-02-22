
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
