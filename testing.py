doc_ref = db.collection("users").document("user1")
doc_ref.set({
    "name": "Alice",
    "age": 25,
    "city": "Hyderabad"
})
