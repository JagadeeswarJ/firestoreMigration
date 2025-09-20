from db import sourceDb as sdb
import json
from google.cloud.firestore_v1 import _helpers

doc_ref = sdb.collection("query_results")
docs = doc_ref.stream()

data = {doc.id: doc.to_dict() for doc in docs}

# Use default=str to convert any non-serializable objects (like DatetimeWithNanoseconds) to strings
with open("backup.json", "w") as f:
    json.dump(data, f, indent=2, default=lambda x: x.isoformat() if hasattr(x, "isoformat") else str(x))
