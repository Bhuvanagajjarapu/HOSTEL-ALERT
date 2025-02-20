import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

# Initialize MongoDB client and collections
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]
resolver_collection = db["resolvers"]

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC3676883f1e3a7200adb7ae6316ba672f"
TWILIO_AUTH_TOKEN = "35743141470e6141b6c4aad729317d14"
TWILIO_PHONE_NUMBER = "+19123190157"

def send_sms_notification(phone_number, message):
    try:
        # Twilio client initialization is missing in your code. Assuming you have already initialized it elsewhere.
        # twilio_client.messages.create(
        #     to=phone_number,
        #     from_=TWILIO_PHONE_NUMBER,
        #     body=message
        # )
        return True
    except Exception as e:
        st.error(f"Error sending SMS: {e}")
        return False

def resolver_home():
    st.title("Resolver Home👨🏻‍🔧")
    
    # Track completed complaints using session_state
    if 'completed_complaints' not in st.session_state:
        st.session_state.completed_complaints = []

    # Display list of complaints
    complaints_cursor = complaint_collection.find({"status": {"$ne": "Completed"}})  # Filter out completed complaints
    for complaint in complaints_cursor:
        if complaint['_id'] not in st.session_state.completed_complaints:
            with st.expander(f"Complaint {complaint['_id']}"):
                display_complaint_details(complaint)

def display_complaint_details(complaint):
    st.subheader("Complaint Details:")
    st.write(f"Student ID: {complaint['student_id']}")
    st.write(f"Hostel: {complaint['hostel']}")
    st.write(f"Room Number: {complaint['room_number']}")
    st.write(f"Email: {complaint['email']}")
    st.write(f"Complaint: {complaint['complaint']}")
    st.write(f"Department: {complaint['department']}")

    with st.form(key=f"form_{complaint['_id']}"):
        st.write("Update Status:")
        status = st.selectbox("Select Status:", ["In Progress", "Completed"])
        st.form_submit_button("Submit")
        if status == "Completed":
            update_complaint_status(complaint['_id'], status)

def update_complaint_status(complaint_id, status):
    complaint_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {"status": status}}
    )
    st.success("Status updated successfully!")
    if status == "Completed":
        st.session_state.completed_complaints.append(complaint_id)  # Add completed complaint to session state

def notify_user(complaint):
    resolver = resolver_collection.find_one({"complaint_id": complaint['complaint_id']})
    if resolver:
        phone_number = resolver.get("phone_number")
        if phone_number:
            message = f"Your complaint with ID {complaint['complaint_id']} has been marked as Completed. Thank you!"
            if send_sms_notification(phone_number, message):
                st.success("User notified successfully.")
            else:
                st.error("Failed to notify user.")
        else:
            st.error("Resolver's phone number is not available.")
    else:
        st.error("Resolver information not found for this complaint.")

resolver_home()