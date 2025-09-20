from db import destinationDb as ddb
import json
from dateutil.parser import isoparse
from datetime import datetime

collection_name = "query_res_backup"

with open("query_results.json", "r") as f:
    data = json.load(f)

def restore(obj):
    if isinstance(obj, str):
        try:
            # Convert ISO string back to datetime object
            dt = isoparse(obj)
            if isinstance(dt, datetime):
                return dt  # Firestore accepts datetime directly
            return obj
        except:
            return obj  # Not a timestamp string
    elif isinstance(obj, dict):
        return {k: restore(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [restore(v) for v in obj]
    return obj

for doc_id, doc_data in data.items():
    print(f"Uploading doc {doc_id}")
    doc_data = restore(doc_data)
    ddb.collection(collection_name).document(doc_id).set(doc_data)

print(f"Uploaded {len(data)} documents to collection '{collection_name}'")
