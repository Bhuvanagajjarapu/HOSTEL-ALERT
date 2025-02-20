import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
login_collection = db["details"]
hostels_collection = db["hostels"]  # Collection for hostels
students_collection = db["students"]  # Collection for students

def username_exists(username):
    return login_collection.find_one({"username": username}) is not None

def add_user(new_username, name, hord, password, email, phone_number, hostel=None, floor=None, room_no=None):
    user_data = {
        "username": new_username,
        "name": name,
        "hord": hord,
        "password": password,
        "email": email,
        "phone_number": phone_number,
        "hostel": hostel,
        "floor": floor,
        "room_no": room_no
    }
    login_collection.insert_one(user_data)
    students_collection.insert_one(user_data)

def get_hostels():
    return hostels_collection.distinct("hostelname")

def get_floor_room_count(hostel_name, floor_number):
    hostel_data = hostels_collection.find_one({"hostelname": hostel_name})
    if hostel_data:
        return hostel_data.get(f"floor{floor_number}", 0)
    return 0

def signup_page():
    st.title("🔐✨ SignUp Page ✨🔐")
    new_username = st.text_input("🆔 Enter your Register Number")
    name = st.text_input("Enter your name")
    hord = st.selectbox("Hosteler or Regular", ["Hosteler", "DayScholar"])
    if hord == "Hosteler":
        hostels = get_hostels()
        hostel = st.selectbox("Choose your hostel", hostels) if hostels else None
        if hostel:
            floor_numbers = [int(floor[5]) for floor in hostels_collection.find_one({"hostelname": hostel}) if floor.startswith("floor")]
            floor = st.selectbox("Choose your floor", floor_numbers) if floor_numbers else None
            if floor:
                room_count = get_floor_room_count(hostel, floor)
                room_numbers = [str(i) for i in range(1, room_count + 1)]
                room_no = st.selectbox("Room no", room_numbers) if room_numbers else None
    
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")

    if new_password != confirm_password:
        st.error("Passwords do not match. Please enter matching passwords.")
        return

    if st.button("Signup"):
        if not username_exists(new_username):
            add_user(new_username, name, hord, new_password, email, phone_number, hostel, floor, room_no)
            st.success("Signup successful! You can now log in.")
        else:
            st.error("Username already exists. Please choose a different username.")

signup_page()