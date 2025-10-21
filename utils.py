import pyrebase
import pandas as pd
import json
import datetime as dt

# Firebase initialization
firebase = None
db = None

def init_firebase(service_account_json):
    global firebase, db
    # Load service account JSON from Streamlit secrets
    config = json.loads(service_account_json)
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

# Initialize Firebase using secrets
# This assumes your Streamlit app imports st first
import streamlit as st
init_firebase(st.secrets["firebase"]["service_account"])

# --- Certificate Functions ---

def add_certificate(cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").push(data)

def get_certificates():
    certs = db.child("certificates").get()
    if certs.each() is None:
        return pd.DataFrame(columns=["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"])
    
    data = []
    for c in certs.each():
        record = c.val()
        record["Key"] = c.key()
        data.append(record)
    df = pd.DataFrame(data)
    # Reorder columns
    df = df[["Key", "Certificate_Number", "Amount", "Issue_Date", "Maturity_Date"]]
    return df

def delete_certificate(key):
    db.child("certificates").child(key).remove()

def edit_certificate(key, cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": float(amount),
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").child(key).update(data)
