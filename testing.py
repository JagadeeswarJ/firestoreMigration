from db import sourceDb as sdb
import json

doc_ref = sdb.collection("query_results")
docs = doc_ref.stream()

for doc in docs:
    print(doc)