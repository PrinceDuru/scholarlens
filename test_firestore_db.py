from google.cloud import firestore
import datetime

# Initialize Firestore using service account key
db = firestore.Client.from_service_account_json("serviceAccount.json")

# Reference a collection and document
doc_ref = db.collection("scholarlens_test").document("demo")

# Write a test document
doc_ref.set({
    "status": "ok",
    "timestamp": datetime.datetime.utcnow().isoformat()
})

# Read it back
result = doc_ref.get()
print("Retrieved document:", result.to_dict())




db = firestore.Client.from_service_account_json("serviceAccount.json")

# Write a simple document
doc_ref = db.collection("demo_collection").document("hello_doc")
doc_ref.set({
    "message": "Hello Firestore!"
})

# Read it back
result = doc_ref.get()
print("Retrieved:", result.to_dict())
