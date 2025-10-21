import pyrebase
import pandas as pd
import json
import streamlit as st

# --- Initialize Firebase ---
def init_firebase_from_secrets():
    # Make a mutable copy of the secrets dictionary
    service_account_details = dict(st.secrets["firebase"])

    # Pyrebase's initialize_app expects the serviceAccount parameter
    # to be the dictionary *containing* the service account credentials directly,
    # not a dictionary where 'serviceAccount' is a key pointing to another dict.
    # So, we pass 'service_account_details' directly as the value for 'serviceAccount'.

    # It also requires a projectId, databaseURL, and potentially others.
    # We construct these from the service_account_details.

    firebase_config = {
        "apiKey": None,  # Not strictly needed for service account auth with Realtime Database
        "authDomain": service_account_details["project_id"] + ".firebaseapp.com",
        "databaseURL": "https://" + service_account_details["project_id"] + ".firebaseio.com",
        "projectId": service_account_details["project_id"],
        "storageBucket": service_account_details["project_id"] + ".appspot.com",
        "messagingSenderId": None, # Replace with actual if you use messaging
        "appId": None, # Replace with actual if you use app id
        "serviceAccount": service_account_details # Pass the actual dictionary here
    }

    # The 'type' key is expected by oauth2client but not specifically removed by pyrebase,
    # so we don't need to delete it. The previous del was an attempt to fix a different issue.
    # The 'type' key with value "service_account" is exactly what it expects.

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
