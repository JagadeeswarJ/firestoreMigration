from db import sourceDb as sdb
import json
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

doc_ref = sdb.collection("query_results")
docs = doc_ref.stream()

def convert(obj):
    if isinstance(obj, DatetimeWithNanoseconds):
        return obj.isoformat()  # Convert timestamp to ISO string
    elif isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert(v) for v in obj]
    return obj

data = {doc.id: convert(doc.to_dict()) for doc in docs}

with open("query_results.json", "w") as f:
    json.dump(data, f, indent=2)
