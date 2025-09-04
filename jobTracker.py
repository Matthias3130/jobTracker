import streamlit as st
import pandas as pd
import os

# --- Setup App ---

# File to store data
DATA_FILE = "applications.csv"

# Load data or create empty
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Company", "Role", "Date Applied", "Method", "Status"])

st.set_page_config(
    page_title="Job Application Tracker",
    layout="wide",  # Makes the app use the full screen width
)

st.markdown(
    "<h1 style='text-align: center;'>Job Application Tracker</h1>",
    unsafe_allow_html=True
)

# --- Website Format ---

cols = st.columns(2)

# --- Applications Features ---

main_container = cols[0].container()
with main_container:
    
    # --- Add New Application ---
    st.header("Add Application")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        company = col1.text_input("Company")
        role = col2.text_input("Role")
        
        col3, col4 = st.columns(2)
        date_applied = col3.date_input("Date Applied")
        method = col4.selectbox("Method", ["Company Site", "LinkedIn", "Indeed", "Referral", "Other"])
        
        status = st.selectbox("Status", ["Pending", "Interview", "Offer", "Rejected"])
        
        submitted = st.form_submit_button("Add")
        if submitted:
            new_data = {"Company": company, "Role": role, "Date Applied": date_applied,
                        "Method": method, "Status": status}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Added {role} at {company}")

    # --- Update Status ---
    st.header("Update Status")
    if not df.empty:
        col1, col2 = st.columns(2)
        selected_company = col1.selectbox("Select Application", df["Company"] + " - " + df["Role"])
        new_status = col2.selectbox("New Status", ["Pending", "Interview", "Offer", "Rejected"])
        if st.button("Update"):
            idx = df.index[(df["Company"] + " - " + df["Role"]) == selected_company][0]
            df.at[idx, "Status"] = new_status
            df.to_csv(DATA_FILE, index=False)
            st.success("Status updated!")

# --- View Applications ---

table_container = cols[1].container()
with table_container:
    st.header("All Applications")
    st.dataframe(df)
    
