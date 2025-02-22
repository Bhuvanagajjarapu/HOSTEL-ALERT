
import streamlit as st
from pymongo import MongoClient
from twilio.rest import Client
from datetime import datetime  

# Initialize MongoDB client and collections
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
hostels_collection = db["hostels"]
complaint_collection = db["complaints"]
login_collection = db["details"]  
technician_collection = db["technicians"]  

# Twilio setup
# secret

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to send SMS notification
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

# Function to get technician's phone number based on department from the database
def get_technician_phone_number_from_db(resolver_type):
    technician = technician_collection.find_one({"resolver_type": resolver_type})
    return technician.get("phonenumber", "") if technician else ""

# Function to display the complaint form
def complaint_form(email):
    user_data = login_collection.find_one({"email": email})

    if user_data:
        student_name = user_data.get("name", "")
        student_id = user_data.get("username", "")
        hostel = user_data.get("hostel", "")
        floor = user_data.get("floor", "")
        room_number = user_data.get("room_no", "")
        phone_number = user_data.get("phone_number", "")

        # Add a logout button on the right side
        left_col, right_col = st.columns([4, 1])  
        with right_col:
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()

        st.title(f"Welcome {student_name}!")
        st.title("Student Complaint Form")

        # Left side: student details
        left_column, right_column = st.columns(2)

        with left_column:
            st.text_input("Student ID", value=student_id, key="student_id", disabled=True)
            st.text_input("Hostel", value=hostel, key="hostel", disabled=True)
            st.text_input("Floor", value=floor, key="floor", disabled=True)

        with right_column:
            st.text_input("Room Number", value=room_number, key="room_number", disabled=True)
            st.text_input("Email", value=email, key="email", disabled=True)
            st.text_input("Phone Number", value=phone_number, key="phone_number", disabled=True)

        st.markdown("---")  # Horizontal line separator
        
        complaint_text = st.text_area("Complaint")
        
        # Fetch available departments from the technicians collection
        departments = technician_collection.distinct("resolver_type")
        department_options = ["CHOOSE DEPARTMENT"] + departments + ["OTHERS"]
        
        department = st.selectbox("Department", department_options)
        
        if department == "OTHERS":
            custom_department = st.text_input("Enter Department")
            if custom_department:
                department = custom_department
                technician_collection.insert_one({"resolver_type": department})  
            else:
                st.warning("Please enter a department.")

        uploaded_file = st.file_uploader("Choose a file")

        # Submission handling
        if st.button("Submit"):
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            complaint_data = {
                "student_name": student_name,
                "student_id": student_id,
                "hostel": hostel,
                "floor": floor,
                "room_number": room_number,
                "email": email,
                "phone_number": phone_number,
                "complaint": complaint_text,
                "department": department,
                "file_content": None,
                "status": "Progress",
                "raised_datetime": current_datetime  
            }

            if uploaded_file is not None:
                file_content = uploaded_file.read()
                complaint_data["file_content"] = file_content

            complaint_collection.insert_one(complaint_data)

            st.success("Complaint submitted successfully!")

            # Send SMS if a valid department was selected
            if department not in ["CHOOSE DEPARTMENT", "OTHERS"]:
                technician_phone_number = get_technician_phone_number_from_db(department)
                
                if technician_phone_number:
                    message = (
                        f"New Complaint Received!\n"
                        f"Student Name: {student_name}\n"
                        f"Student ID: {student_id}\n"
                        f"Hostel: {hostel}\n"
                        f"Floor: {floor}\n"
                        f"Room Number: {room_number}\n"
                        f"Email: {email}\n"
                        f"Phone Number: {phone_number}\n"
                        f"Complaint: {complaint_text}\n"
                        f"Department: {department}\n"
                        f"Raised Date and Time: {current_datetime}\n"
                        "Please check and resolve."
                    )
                    send_sms_notification(technician_phone_number, message)
                else:
                    st.warning(f"No technician found for department: {department}")

    else:
        st.error("User data not found!")
