import os
import firebase_admin
from firebase_admin import credentials, firestore


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
try:
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase app initialized successfully")
except Exception as e:
    print(f"Error initializing Firebase: {e}")
