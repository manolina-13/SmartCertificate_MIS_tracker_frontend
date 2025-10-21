import pyrebase
import pandas as pd
import json
import streamlit as st

# --- Initialize Firebase ---
def init_firebase_from_secrets():
    # Make a mutable copy of the secrets dictionary
    service_account_details = dict(st.secrets["firebase"])

    # Pyrebase requires an API key, but it's not strictly used for service account authentication
    # for a Realtime Database setup. We'll set it to None as a placeholder.
    # Also, populate other fields from the service_account_details.
    firebase_config = {
        "apiKey": None,
        "authDomain": service_account_details["project_id"] + ".firebaseapp.com",
        "databaseURL": "https://" + service_account_details["project_id"] + ".firebaseio.com",
        "projectId": service_account_details["project_id"],
        "storageBucket": service_account_details["project_id"] + ".appspot.com",
        "messagingSenderId": None, # Replace with actual if you use messaging
        "appId": None, # Replace with actual if you use app id
        "serviceAccount": service_account_details
    }
    
    # Remove "type" from the service account dict if it's there, as pyrebase expects specific keys
    if "type" in firebase_config["serviceAccount"]:
        del firebase_config["serviceAccount"]["type"]

    firebase = pyrebase.initialize_app(firebase_config)
    global db
    db = firebase.database()

# Call initialization
init_firebase_from_secrets()

# --- CRUD Operations ---
def add_certificate(cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").push(data)

def get_certificates():
    data = db.child("certificates").get()
    if data.each():
        df = pd.DataFrame([{
            "Key": item.key(),
            **item.val()
        } for item in data.each()])
        return df
    return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])

def delete_certificate(key):
    db.child("certificates").child(key).remove()

def edit_certificate(key, cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").child(key).update(data)
