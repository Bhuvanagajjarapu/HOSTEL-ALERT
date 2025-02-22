
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["project"]
complaint_collection = db["complaints"]

# Function to generate MongoDB query using LLM
def get_mongo_query(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to fetch complaints based on the generated query
def get_complaints(query):
    try:
        mongo_query = eval(query)  # Convert string to dictionary
        complaints = list(complaint_collection.find(mongo_query, {"_id": 0}))
        return complaints
    except Exception as e:
        return str(e)

# LLM Prompt
prompt = [
    """
    You are an expert in converting English questions to MongoDB queries!
    The database 'project' has a collection 'complaints' with fields:
    - student_name (String)
    - student_id (String)
    - hostel (String)
    - room_number (String)
    - complaint (String)
    - department (String)
    
    Convert user queries into MongoDB queries.
    Example 1: "Show me complaints from Saradha Hostel"
    Output: {"hostel": "Saradha"}
    
    Example 2: "What are the complaints related to plumbing?"
    Output: {"department": "Plumbing"}
    
    Do not include any extra text in the response. Only return the query in dictionary format.
    """
]

# Set Streamlit page configuration
st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Top Bar with Logout Button
col1, col2 = st.columns([8, 1])  # Allocating space for title and logout button
with col2:
    if st.button("Logout", key="logout"):
        st.session_state.clear()
        st.rerun()  # Refresh the page after logout

st.title("Admin Dashboard - Complaints")

# Input and Query Submission
question = st.text_input("Ask a query about complaints:", key="input")
submit = st.button("Get Complaints")

if submit and question:
    query = get_mongo_query(question, prompt)
    complaints = get_complaints(query)

    if isinstance(complaints, list) and complaints:
        # Convert data to DataFrame
        df = pd.DataFrame(complaints)

        # Ensure columns are properly ordered
        expected_columns = ["student_name", "student_id", "hostel", "room_number", "complaint", "department"]
        
        # Ensure missing columns don't cause errors
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None  # Add missing columns with None values

        df = df[expected_columns]  # Reorder columns

        # Replace 'CHOOSE DEPARTMENT' with 'Not Assigned' for clarity
        df["department"] = df["department"].replace("CHOOSE DEPARTMENT", "Not Assigned")

        # Display data in table format
        st.subheader("Complaints List")
        st.dataframe(df)  # Display as a table
    else:
        st.info("No complaints found for the given query.")

