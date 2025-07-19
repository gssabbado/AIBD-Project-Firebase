import streamlit as st
import json
import firebase_admin
import pandas as pd
import requests
from firebase_admin import credentials
from firebase_admin import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("key.json")

# Create a reference to the Google post.
doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())