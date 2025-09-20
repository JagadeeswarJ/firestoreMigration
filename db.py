import firebase_admin
from firebase_admin import credentials, firestore

SourceCred = credentials.Certificate("keys/source-serviceAccountKey.json")
DestinationCred = credentials.Certificate("keys/destination-serviceAccountKey.json")

source_app = firebase_admin.initialize_app(SourceCred, name="source")
destination_app = firebase_admin.initialize_app(DestinationCred, name="destination")

sourceDb = firestore.client(app=source_app)
destinationDb = firestore.client(app=destination_app)
