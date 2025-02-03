from database.firebase_setup import db
from firebase_admin import auth

def verify_firebase_token(token: str):
    return auth.verify_id_token(token, clock_skew_seconds=60)

def fetch_user_by_uid(uid: str):
    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return None
    return user_doc


def get_user_by_email(email: str):
    user_ref = db.collection("users").where("email", "==", email).limit(1).get()
    if user_ref:
        return user_ref[0].to_dict()
    else:
        return None