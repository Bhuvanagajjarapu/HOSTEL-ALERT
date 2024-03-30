import streamlit as st
from pymongo import MongoClient
from twilio.rest import Client


client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]

ALLOWED_RESOLVER_NUMBERS = {
    "8919542599": "ELECTRICIAN",
    "9550676575": "HOUSEKEEPER",
    "7382944698": "TECHSUPPORT",
    "7382904875": "PLUMBER",
    "9908268058": "AC REPAIR"
}

def resolver_home(resolver_type):
    st.title(f"{resolver_type} Resolver Home")

   
    fetch_and_display_complaints(resolver_type)

def fetch_and_display_complaints(resolver_type):
    st.subheader("List of Complaints:")
    
   
    complaints_cursor = complaint_collection.find({"department": resolver_type})
    i = 1
    for complaint in complaints_cursor:
       
        st.markdown(
            f"""
            <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; border-radius: 5px; font-family: 'Arial', sans-serif;">
                <p style="font-weight: bold; font-size: 18px; color: #333;">Complaint {i}</p>
                <p><strong>Complaint ID:</strong> {complaint['complaint_id']}</p>
                <p><strong>Student Name:</strong> {complaint['student_name']}</p>
                <p><strong>Student ID:</strong> {complaint['student_id']}</p>
                <p><strong>Hostel:</strong> {complaint['hostel']}</p>
                <p><strong>Room Number:</strong> {complaint['room_number']}</p>
                <p><strong>Email:</strong> {complaint['email']}</p>
                <p><strong>Complaint:</strong> {complaint['complaint']}</p>
                <p><strong>Department:</strong> {complaint['department']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        i += 1

client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
resolver_collection = db["resolvers"]
TWILIO_ACCOUNT_SID = "AC3676883f1e3a7200adb7ae6316ba672f"
TWILIO_AUTH_TOKEN = "35743141470e6141b6c4aad729317d14"
TWILIO_PHONE_NUMBER = "+19123190157"
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_notification(phone_number, message):
    try:
        twilio_client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message
        )
        return True
    except Exception as e:
        st.error(f"Error sending SMS: {e}")
        return False

def resolver_form():
    st.title("Resolver Form")
    complaint_id = st.text_input("Complaint ID")
    status_options = ["In Progress", "Completed"]
    status = st.selectbox("Status", status_options)

    department_options = ["ELECTRICIAN", "PLUMBER", "HOUSEKEEPING","TECHSUPPOURT","AC REPAIR"]  # Add your department names
    department = st.selectbox("Department", department_options)

    phone_number = st.text_input("client's Phone Number")

    if st.button("Update Status"):
      
        if complaint_id.isdigit():
            complaint_id = int(complaint_id)
            resolver_complaint = {"complaint_id": complaint_id, "status": status, "department": department}
            resolver_collection.insert_one(resolver_complaint)
            message = f"Complaint ID {complaint_id} status updated to {status} in Resolver database for {department} department!"
            send_sms_notification(phone_number, message)

            st.success(message)
        else:
            st.error("Invalid complaint ID. Please enter a valid number.")



def resolver_page():
    st.title("Resolver Page")
    st.write("Enter your phone number to log in:")
    phone_number = st.text_input("Phone Number")

    if st.button("Click Here"):
       
        if phone_number in ALLOWED_RESOLVER_NUMBERS:
            resolver_type = ALLOWED_RESOLVER_NUMBERS[phone_number]
            st.session_state.resolver_authenticated = True
            st.session_state.resolver_phone_number = phone_number
            st.session_state.resolver_type = resolver_type

           
            st.success(f"Logged in as {resolver_type} with phone number {phone_number}")

    
            resolver_home(resolver_type)
            resolver_form()

            
            st.markdown(f"[Click here to go to Resolver Home](#resolver-home)", unsafe_allow_html=True)

        else:
            st.error("Invalid phone number. Please try again.")

if __name__ == "__main__":
    resolver_page()
