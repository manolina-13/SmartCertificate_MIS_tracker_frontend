import streamlit as st
import pandas as pd
import datetime as dt
from utils import add_certificate, get_certificates, delete_certificate, edit_certificate

st.set_page_config(page_title="MIS Certificate Tracker", layout="centered")
st.title("📜 MIS Certificate Tracker")

# --- Form to Add Certificate ---
with st.form("mis_form"):
    cert_no = st.text_input("Certificate Number")
    amount = st.number_input("Amount (₹)", min_value=0.0)
    issue_date = st.date_input("Issue Date")
    maturity_date = st.date_input("Maturity Date")
    submitted = st.form_submit_button("Add Certificate")
    
    if submitted:
        add_certificate(cert_no, amount, issue_date, maturity_date)
        st.success("✅ Certificate added successfully!")

# --- Display Certificates ---
st.subheader("📅 All Certificates")
df = get_certificates()

# Calculate Days Left
df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
df["Days_Left"] = (df["Maturity_Date"].dt.date - dt.date.today()).apply(lambda x: x.days)

# Highlight certificates <=10 days
def highlight_due(row):
    return ['background-color: #FFCCCC' if row.Days_Left <= 10 else '' for _ in row]

# Display full table with highlight
st.dataframe(df.style.apply(highlight_due, axis=1))

# Show warning table for due certificates
due = df[df["Days_Left"] <= 10]
if not due.empty:
    st.warning("⚠️ Certificates maturing soon!")
    st.dataframe(due.drop(columns=["Key"]))

# --- Edit/Delete Section ---
st.subheader("✏️ Edit or Delete Certificate")
if not df.empty:
    options = df["Certificate_Number"] + " | " + df["Amount"].astype(str)
    selected = st.selectbox("Select certificate", options)
    key = df.loc[df["Certificate_Number"] == selected.split(" | ")[0], "Key"].values[0]

    # Delete button
    if st.button("Delete"):
        delete_certificate(key)
        st.success("🗑️ Certificate deleted successfully!")

    # Edit form
    with st.form("edit_form"):
        new_cert_no = st.text_input("Certificate Number", value=df.loc[df["Key"]==key, "Certificate_Number"].values[0])
        new_amount = st.number_input("Amount", value=float(df.loc[df["Key"]==key, "Amount"].values[0]))
        new_issue = st.date_input("Issue Date", value=pd.to_datetime(df.loc[df["Key"]==key, "Issue_Date"].values[0]))
        new_maturity = st.date_input("Maturity Date", value=pd.to_datetime(df.loc[df["Key"]==key, "Maturity_Date"].values[0]))
        submitted_edit = st.form_submit_button("Save Changes")
        
        if submitted_edit:
            edit_certificate(key, new_cert_no, new_amount, new_issue, new_maturity)
            st.success("✏️ Certificate updated successfully!")
