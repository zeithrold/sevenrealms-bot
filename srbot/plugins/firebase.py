import firebase_admin
from firebase_admin import firestore_async

app = firebase_admin.initialize_app()
db = firestore_async.client(app)
