import pandas as pd
from datetime import datetime
import pyrebase

# ----------------- Initialize Firebase -----------------
firebase_config = None
db = None

def init_firebase(config):
    """
    Call this from app.py to initialize Firebase once
    """
    global firebase_config, db
    firebase_config = config
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

# ----------------- Certificate Functions -----------------
def add_certificate(cert_no, amount, issue_date, maturity_date):
    record = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": issue_date.strftime("%Y-%m-%d"),
        "Maturity_Date": maturity_date.strftime("%Y-%m-%d")
    }
    db.child("certificates").push(record)

def get_certificates():
    data = db.child("certificates").get()
    if data.each() is None:
        return pd.DataFrame(columns=["Certificate_Number", "Amount", "Issue_Date", "Maturity_Date", "Key"])
    
    records = []
    for item in data.each():
        record = item.val()
        record["Key"] = item.key()
        records.append(record)
    df = pd.DataFrame(records)
    return df

def delete_certificate(key):
    db.child("certificates").child(key).remove()

def edit_certificate(key, cert_no, amount, issue_date, maturity_date):
    record = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": issue_date.strftime("%Y-%m-%d"),
        "Maturity_Date": maturity_date.strftime("%Y-%m-%d")
    }
    db.child("certificates").child(key).update(record)
