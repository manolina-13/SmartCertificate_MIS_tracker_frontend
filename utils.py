import pyrebase
import pandas as pd
import json

# --- Initialize Firebase ---
def init_firebase(service_account_json):
    config = json.loads(service_account_json)
    firebase = pyrebase.initialize_app(config)
    global db
    db = firebase.database()

# Call initialization
import streamlit as st
init_firebase(st.secrets["firebase"]["service_account"])

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
