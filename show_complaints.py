import streamlit as st
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]
technician_collection = db["technicians"]

# Function to fetch departments from the database
def get_departments():
    departments = technician_collection.distinct("department")
    return departments

# Function to fetch complaints for a specific hostel and department
def get_complaints_for_hostel_and_department(hostel, department):
    query = {"hostel": hostel}
    if department:
        query["department"] = department
    complaints = list(complaint_collection.find(query, {"_id": 0, "student_name": 1, "student_id": 1, "room_number": 1, "complaint": 1, "department": 1}))
    
    # Fetch department information from technicians collection
    technician_department = technician_collection.find_one({"hostel": hostel, "department": department}, {"_id": 0, "department": 1})
    if technician_department:
        department_name = technician_department.get("department")
        for complaint in complaints:
            complaint["department"] = department_name
    
    return complaints

# New page function
def show_complaints():
    st.title("Welcome")

    # Select hostel
    st.write("Select a hostel:")
    hostels = complaint_collection.distinct("hostel")
    selected_hostel = st.selectbox("Hostel", hostels)

    # Select department
    st.write("Select a department (optional):")
    departments = [""] + get_departments()  # Populate departments from the database
    selected_department = st.selectbox("Department", departments)

    # Fetch and display complaints
    if selected_hostel:
        st.write(f"Complaints for {selected_hostel}:")
        complaints = get_complaints_for_hostel_and_department(selected_hostel, selected_department)
        for complaint in complaints:
            st.write(f"Student Name: {complaint['student_name']}, Student ID: {complaint['student_id']}, Room Number: {complaint['room_number']}, Complaint: {complaint['complaint']}, Department: {complaint['department']}")

# Call the function to display the new page
if __name__ == "_main_":
    show_complaints()