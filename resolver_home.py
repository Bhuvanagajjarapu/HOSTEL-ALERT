# import streamlit as st
# from pymongo import MongoClient
# from bson import ObjectId
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # MongoDB Connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["project"]
# complaint_collection = db["complaints"]

# # Email Configuration
# EMAIL_SENDER = "gajjarapubhuvana@gmail.com"
# EMAIL_PASSWORD = "uhgf gktr rcsn jwst"

# def send_email_notification(to_email, subject, message):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = to_email
#         msg["Subject"] = subject
#         msg.attach(MIMEText(message, "plain"))

#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#         server.quit()
        
#         return True
#     except Exception as e:
#         st.error(f"Error sending email: {e}")
#         return False

# def resolver_home():
#     st.title("Resolver Home 👨🏻‍🔧")

#     # Ensure resolver is authenticated
#     if "resolver_authenticated" not in st.session_state or not st.session_state.resolver_authenticated:
#         st.error("You must log in first!")
#         return

#     resolver_type = st.session_state.resolver_type

#     st.subheader(f"Viewing complaints for: {resolver_type}")

#     # Fetch only complaints for the logged-in resolver's department
#     complaints_cursor = complaint_collection.find({"department": resolver_type, "status": {"$ne": "Completed"}})

#     if complaint_collection.count_documents({"status": {"$ne": "Completed"}}) == 0:

#         st.info("No pending complaints for your department.")
#         return

#     for complaint in complaints_cursor:
#         with st.expander(f"Complaint {complaint['_id']}"):
#             display_complaint_details(complaint)

# def display_complaint_details(complaint):
#     st.subheader("Complaint Details:")
#     st.write(f"👤 Student Name: {complaint['student_name']}")
#     st.write(f"🏠 Hostel: {complaint['hostel']}")
#     st.write(f"🔢 Room Number: {complaint['room_number']}")
#     st.write(f"📧 Email: {complaint['email']}")
#     st.write(f"🔧 Department: {complaint['department']}")
#     st.write(f"📝 Complaint: {complaint['complaint']}")

#     with st.form(key=f"form_{complaint['_id']}"):
#         status = st.selectbox("Update Status:", ["In Progress", "Completed"])
#         submit = st.form_submit_button("Submit")

#         if submit:
#             update_complaint_status(complaint, status)

# def update_complaint_status(complaint, status):
#     complaint_id = complaint['_id']
#     student_name = complaint['student_name']
#     student_email = complaint['email']
#     department = complaint['department']
#     complaint_text = complaint['complaint']

#     if status == "Completed":
#         complaint_collection.delete_one({"_id": ObjectId(complaint_id)})
#         st.session_state.completed_complaints.append(complaint_id)
#     else:
#         complaint_collection.update_one(
#             {"_id": ObjectId(complaint_id)},
#             {"$set": {"status": status}}
#         )

#     st.success(f"Status updated to '{status}' successfully!")

#     # Email Subject: Complaint ID (ObjectId)
#     subject = f"Complaint Update - {complaint_id}"

#     # Email Body
#     message = f"""
#     Hello {student_name},

#     Your complaint regarding {department} has been updated.
    
#     🏠 Issue: {complaint_text}
#     ✅ Status: {status}
    
#     A technician has reviewed your complaint. Thank you!
#     """

#     if send_email_notification(student_email, subject, message):
#         st.success(f"Email notification sent to {student_email}.")
#     else:
#         st.error("Failed to send email notification.")

# if __name__ == "__main__":
#     resolver_home()
import streamlit as st
from pymongo import MongoClient
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]

# Email Configuration
EMAIL_SENDER = "gajjarapubhuvana@gmail.com"
EMAIL_PASSWORD = "uhgf gktr rcsn jwst"

def send_email_notification(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def resolver_home():
    st.title("Resolver Dashboard 👨🏻‍🔧")

    if not st.session_state.resolver_authenticated:
        st.error("You must log in first!")
        return

    resolver_type = st.session_state.resolver_type
    st.subheader(f"Complaints for: {resolver_type}")

    complaints_cursor = complaint_collection.find({"department": resolver_type, "status": {"$ne": "Completed"}})

    if complaint_collection.count_documents({"status": {"$ne": "Completed"}}) == 0:
        st.info("No pending complaints for your department.")
        return

    for complaint in complaints_cursor:
        with st.expander(f"Complaint {complaint['_id']}"):
            st.write(f"👤 **Student Name:** {complaint['student_name']}")
            st.write(f"🏠 **Hostel:** {complaint['hostel']}")
            st.write(f"📧 **Email:** {complaint['email']}")
            st.write(f"📝 **Complaint:** {complaint['complaint']}")

            with st.form(key=f"form_{complaint['_id']}"):
                status = st.selectbox("Update Status:", ["In Progress", "Completed"])
                submit = st.form_submit_button("Submit")

                if submit:
                    update_complaint_status(complaint, status)

def update_complaint_status(complaint, status):
    complaint_id = complaint['_id']
    student_email = complaint["email"]
    student_name = complaint["student_name"]
    complaint_text = complaint["complaint"]

    if status == "Completed":
        complaint_collection.delete_one({"_id": ObjectId(complaint_id)})
        st.success(f"Complaint {complaint_id} marked as 'Completed' and removed from the list.")
    else:
        complaint_collection.update_one({"_id": ObjectId(complaint_id)}, {"$set": {"status": status}})
        st.success(f"Status updated to '{status}' successfully!")

    # Email Subject
    subject = f"Complaint Update - {complaint_id}"

    # Email Body
    message = f"""
    Hello {student_name},

    Your complaint regarding the following issue has been updated.

    🏠 **Issue:** {complaint_text}
    ✅ **Status:** {status}

    Thank you for your patience.

    Regards,  
    Hostel Management Team
    """

    if send_email_notification(student_email, subject, message):
        st.success(f"Email notification sent to {student_email}.")
    else:
        st.error("Failed to send email notification.")

if __name__ == "__main__":
    resolver_home()
