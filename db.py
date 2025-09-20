import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key file
cred = credentials.Certificate("path/to/serviceAccountKeySource.json")

# Initialize app
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()
