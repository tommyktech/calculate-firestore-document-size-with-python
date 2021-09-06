import firebase_admin
from firebase_admin import firestore
import datetime
from google.cloud.firestore_v1._helpers import GeoPoint
from google.cloud.firestore_v1.document import DocumentReference

# calculates document size
def calc_document_size(doc):
    total = 0

    # calculates document path size
    path_arr = doc.reference.path.split("/")
    for path in path_arr:
        total += len(path) + 1
    total += 16

    # calculates the size of each item and sums up the figures
    doc_dict = doc.to_dict()
    for key, value in doc_dict.items():
        total += len(key) + 1
        total += calc_value_size(value)

    return total

# calculates value size of a docuemnt 
def calc_value_size(value):
    if type(value) == str:
        return len(value) + 1
    
    if type(value) == list:
        total = 0
        for datum in value:
            total += calc_value_size(datum)
        return total
    
    if type(value) == bool or value is None:
        return 1

    if type(value) == bytes:
        return len(bytes)

    if isinstance(value, datetime.datetime):
        return 8

    if type(value) in [float, int]:
        return 8
        
    if isinstance(value, GeoPoint):
        return 16

    if isinstance(value, dict):
        total = 0
        for k, v in value.items():
            total += len(k) + 1
            total += calc_value_size(v)
        return total

    if isinstance(value, DocumentReference):
        path_arr = value.path.split("/")
        total = 0
        for path in path_arr:
            total += len(path) + 1
        total += 16
        return total

# initialize firebase client
firebase_admin.initialize_app()
db = firestore.client()

# get document
collection_id = "collection_id"
document_id = "document_id"
doc = db.collection(collection_id).document(document_id).get()

# calculate it's size
size = calc_document_size(doc)
print(size)
