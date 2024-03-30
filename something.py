import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]
resolver_collection = db["resolvers"]

TWILIO_ACCOUNT_SID = "AC3676883f1e3a7200adb7ae6316ba672f"
TWILIO_AUTH_TOKEN = "35743141470e6141b6c4aad729317d14"
TWILIO_PHONE_NUMBER = "+19123190157"

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

def resolver_home():
    st.title("Resolver Home")
    fetch_and_display_complaints()

def fetch_and_display_complaints():
    st.subheader("List of Complaints:")
    
    complaints_cursor = complaint_collection.find()

    buttons = []
    for complaint in complaints_cursor:
        checkbox_state = st.checkbox(f"Complaint ID: {complaint['complaint_id']} - Student Name: {complaint['student_name']}")
        if checkbox_state:
            st.write(f"Student ID: {complaint['student_id']}")
            st.write(f"Hostel: {complaint['hostel']}")
            st.write(f"Room Number: {complaint['room_number']}")
            st.write(f"Email: {complaint['email']}")
            st.write(f"Complaint: {complaint['complaint']}")
            st.write(f"Department: {complaint['department']}")
            open_button = st.button("Open")
            if open_button:
                with st.form(key=f"form_{complaint['_id']}"):
                    st.write("Update Status:")
                    status = st.selectbox("Select Status:", ["In Progress", "Completed"])
                    submit_button = st.form_submit_button("Submit")
                    if submit_button:
                        update_complaint_status(complaint['_id'], status)
                        if status == "Completed":
                            notify_user(complaint)
        buttons.append(st.button(f"Button for {complaint['complaint_id']}"))  # Placeholder button

    # Display buttons after the loop
    st.write("Buttons:")
    for button in buttons:
        if button:
            st.write("Button clicked!")
    
def update_complaint_status(complaint_id, status):
    complaint_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {"status": status}}
    )
    st.success("Status updated successfully!")

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