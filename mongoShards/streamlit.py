import streamlit as st
from pymongo import MongoClient
import json

# Configure MongoDB connection
MONGO_URI = "mongodb://mongos:27017"
DB_NAME = "testDB"
COLLECTION_NAME = "tweets"

# Initialize MongoDB client
def get_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db

# Streamlit app
def main():
    st.title("Simple MongoDB Streamlit App")

    db = get_db()
    print("Connected to MongoDB", db.name)
    col = db.tweets
    print("Using collection", col.count_documents({}))

    # Section: Display first 10 documents
    st.header("Display First 10 Documents")
    if st.button("Load Documents"):
        docs = list(col.find().limit(10))
        if docs:
            for doc in docs:
                st.json(doc)
        else:
            st.write("No documents found.")

    st.markdown("---")

    # Section: Insert new document
    st.header("Insert New Document")
    with st.form(key="insert_form"):
        raw_json = st.text_area("Enter JSON document:", height=200)
        submitted = st.form_submit_button("Insert Document")
        if submitted:
            try:
                data = json.loads(raw_json)
                result = col.insert_one(data)
                st.success(f"Inserted document with id: {result.inserted_id}")
            except Exception as e:
                st.error(f"Error inserting document: {e}")

if __name__ == "__main__":
    main()
