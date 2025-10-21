import streamlit as st
import pandas as pd
import datetime as dt
from utils import add_certificate, get_certificates, delete_certificate, edit_certificate

st.set_page_config(page_title="MIS Certificate Tracker", layout="centered")
st.title("📜 MIS Certificate Tracker")

# --- Form to Add Certificate ---
with st.form("mis_form"):
    st.subheader("Add New Certificate")
    cert_no = st.text_input("Certificate Number")
    amount = st.number_input("Amount (₹)", min_value=0.0)
    issue_date = st.date_input("Issue Date", value=dt.date.today())
    maturity_date = st.date_input("Maturity Date", value=dt.date.today() + dt.timedelta(days=365)) # Default to 1 year later
    submitted = st.form_submit_button("Add Certificate")
    
    if submitted:
        if cert_no and amount > 0:
            add_certificate(cert_no, amount, issue_date, maturity_date)
            st.success("✅ Certificate added successfully!")
            st.experimental_rerun() # Re-run to refresh the certificate list and clear the form
        else:
            st.error("Please fill in all fields correctly (Certificate Number cannot be empty, Amount must be greater than 0).")

# --- Display Certificates ---
st.subheader("📅 All Certificates")
df = get_certificates()

# Calculate Days Left
if not df.empty:
    df["Maturity_Date"] = pd.to_datetime(df["Maturity_Date"])
    df["Issue_Date"] = pd.to_datetime(df["Issue_Date"]) # Ensure Issue_Date is also datetime for consistency
    df["Days_Left"] = (df["Maturity_Date"].dt.date - dt.date.today()).apply(lambda x: x.days)

    # Reorder columns for better display
    df = df[["Certificate_Number", "Amount", "Issue_Date", "Maturity_Date", "Days_Left", "Key"]]

    # Highlight certificates <=10 days
    def highlight_due(row):
        return ['background-color: #FFCCCC' if row.Days_Left <= 10 else '' for _ in row]

    # Display full table with highlight
    st.dataframe(df.style.apply(highlight_due, axis=1), hide_index=True) # hide_index for cleaner look

    # Show warning table for due certificates
    due = df[df["Days_Left"] <= 10]
    if not due.empty:
        st.warning("⚠️ Certificates maturing soon!")
        st.dataframe(due.drop(columns=["Key"]), hide_index=True) # Drop 'Key' and hide index for warning table

# --- Edit/Delete Section ---
st.subheader("✏️ Edit or Delete Certificate")
if not df.empty:
    # Use a unique key for the selectbox to avoid conflicts if you add more selectboxes later
    options = df["Certificate_Number"] + " | Amount: " + df["Amount"].astype(str) + " | Maturity: " + df["Maturity_Date"].dt.strftime("%Y-%m-%d")
    
    selected_option = st.selectbox("Select certificate to edit/delete", options, key="cert_selector")
    
    # Get the key of the selected certificate
    selected_cert_no = selected_option.split(" | ")[0]
    key = df.loc[df["Certificate_Number"] == selected_cert_no, "Key"].values[0]

    # Get current values for the selected certificate for pre-filling the edit form
    current_cert_data = df.loc[df["Key"] == key].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        # Delete button
        if st.button("Delete Selected Certificate", type="secondary"):
            delete_certificate(key)
            st.success(f"🗑️ Certificate '{selected_cert_no}' deleted successfully!")
            st.experimental_rerun() # Re-run to refresh the certificate list

    with col2:
        # Edit form
        with st.form("edit_form"):
            st.markdown("### Edit Details")
            new_cert_no = st.text_input("Certificate Number", value=current_cert_data["Certificate_Number"])
            new_amount = st.number_input("Amount (₹)", value=float(current_cert_data["Amount"]), min_value=0.0)
            new_issue = st.date_input("Issue Date", value=current_cert_data["Issue_Date"].date())
            new_maturity = st.date_input("Maturity Date", value=current_cert_data["Maturity_Date"].date())
            submitted_edit = st.form_submit_button("Save Changes")
            
            if submitted_edit:
                if new_cert_no and new_amount > 0:
                    edit_certificate(key, new_cert_no, new_amount, new_issue, new_maturity)
                    st.success(f"✏️ Certificate '{new_cert_no}' updated successfully!")
                    st.experimental_rerun() # Re-run to refresh the certificate list
                else:
                    st.error("Please fill in all fields correctly (Certificate Number cannot be empty, Amount must be greater than 0).")
else:
    st.info("No certificates to display. Add one using the form above!")
