import pyrebase
import pandas as pd

# Firebase configuration
firebase_config = st.secrets["firebase"]

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Add new certificate
def add_certificate(cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").push(data)

# Get all certificates
def get_certificates():
    data = db.child("certificates").get().val()
    if not data:
        return pd.DataFrame(columns=["Key","Certificate_Number","Amount","Issue_Date","Maturity_Date"])
    df = pd.DataFrame(data.values())
    df["Key"] = list(data.keys())
    return df[["Key","Certificate_Number","Amount","Issue_Date","Maturity_Date"]]

# Delete certificate
def delete_certificate(cert_key):
    db.child("certificates").child(cert_key).remove()

# Edit certificate
def edit_certificate(cert_key, cert_no, amount, issue_date, maturity_date):
    data = {
        "Certificate_Number": cert_no,
        "Amount": amount,
        "Issue_Date": str(issue_date),
        "Maturity_Date": str(maturity_date)
    }
    db.child("certificates").child(cert_key).update(data)
