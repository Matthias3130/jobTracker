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
    df = pd.DataFrame(columns=[
    "Company", 
    "Role", 
    "Location", 
    "Date Applied", 
    "Method", 
    "Status", 
    "Follow-up Date", 
    "Interview Date", 
    "Job Posting URL", 
    "Notes"
])

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
        location = col3.text_input("Location")
        date_applied = col4.date_input("Date Applied")

        col5, col6 = st.columns(2)
        method = col5.selectbox("Method", ["Company Site", "LinkedIn", "Indeed", "Referral", "Other"])
        status = col6.selectbox("Status", ["Pending", "Interview", "Offer", "Rejected"])

        col7, col8 = st.columns(2)
        follow_up_date = col7.date_input("Follow-up Date")
        interview_date = col8.date_input("Interview Date")

        job_url = st.text_input("Job Posting URL")
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add")
        if submitted:
            new_data = {
                "Company": company,
                "Role": role,
                "Location": location,
                "Date Applied": date_applied,
                "Method": method,
                "Status": status,
                "Follow-up Date": follow_up_date,
                "Interview Date": interview_date,
                "Job Posting URL": job_url,
                "Notes": notes
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Added {role} at {company}")

    # --- Update Status ---
    st.header("Update Status")
    if not df.empty:
        col1, col2 = st.columns(2)

        # Create a display string to select the application
        df["Display"] = (
            df["Company"] + " - " + df["Role"] + " (" + df["Location"] + ")"
        )
        selected_app = col1.selectbox("Select Application", df["Display"])

        # Get the index of the selected application
        idx = df.index[df["Display"] == selected_app][0]

        # Pre-fill fields with current values
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            company = col1.text_input("Company", df.at[idx, "Company"])
            role = col2.text_input("Role", df.at[idx, "Role"])

            col3, col4 = st.columns(2)
            location = col3.text_input("Location", df.at[idx, "Location"])
            date_applied = col4.date_input("Date Applied", pd.to_datetime(df.at[idx, "Date Applied"]))

            col5, col6 = st.columns(2)
            method = col5.selectbox(
                "Method", ["Company Site", "LinkedIn", "Indeed", "Referral", "Other"],
                index=["Company Site", "LinkedIn", "Indeed", "Referral", "Other"].index(df.at[idx, "Method"])
            )
            status = col6.selectbox(
                "Status", ["Pending", "Interview", "Offer", "Rejected"],
                index=["Pending", "Interview", "Offer", "Rejected"].index(df.at[idx, "Status"])
            )

            col7, col8 = st.columns(2)
            follow_up_date = col7.date_input("Follow-up Date", pd.to_datetime(df.at[idx, "Follow-up Date"]))
            interview_date = col8.date_input("Interview Date", pd.to_datetime(df.at[idx, "Interview Date"]))

            job_url = st.text_input("Job Posting URL", df.at[idx, "Job Posting URL"])
            notes = st.text_area("Notes", df.at[idx, "Notes"])

            submitted = st.form_submit_button("Update")
            if submitted:
                # Update all fields
                df.at[idx, "Company"] = company
                df.at[idx, "Role"] = role
                df.at[idx, "Location"] = location
                df.at[idx, "Date Applied"] = date_applied
                df.at[idx, "Method"] = method
                df.at[idx, "Status"] = status
                df.at[idx, "Follow-up Date"] = follow_up_date
                df.at[idx, "Interview Date"] = interview_date
                df.at[idx, "Job Posting URL"] = job_url
                df.at[idx, "Notes"] = notes

                df.to_csv(DATA_FILE, index=False)
                st.success(f"Application updated for {company} - {role}")

        # Drop the temporary display column
        df = df.drop(columns=["Display"])

# --- View Applications ---

table_container = cols[1].container()
with table_container:
    st.header("All Applications")
    
    # Select columns to display (omit the last two)
    display_df = df.drop(columns=["Job Posting URL", "Notes", "Follow-up Date"])
    
    st.dataframe(display_df)
    
