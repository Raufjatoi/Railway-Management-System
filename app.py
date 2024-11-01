import streamlit as st
import sqlite3
from database import create_database, add_train, view_trains, edit_train, delete_train

# Initialize the database
create_database()

st.title("Railway Management System")

# Add Train Section
if st.sidebar.button("Add Train"):
    st.header("Add a New Train")
    train_id = st.number_input("Train ID", min_value=1, step=1)
    name = st.text_input("Train Name")
    train_type = st.selectbox("Train Type", ["Express", "Local"])
    start_time = st.text_input("Start Time (e.g., 08:00 AM)")
    end_time = st.text_input("End Time (e.g., 10:00 AM)")

    if st.button("Submit"):
        add_train(train_id, name, train_type, start_time, end_time)
        st.success("Train added successfully!")

# View Trains Section
if st.sidebar.button("View Trains"):
    st.header("Train List")
    trains = view_trains()
    for train in trains:
        st.write(f"ID: {train[0]}, Name: {train[1]}, Type: {train[2]}, Start: {train[3]}, End: {train[4]}")

# Edit Train Section
if st.sidebar.button("Edit Train"):
    st.header("Edit Train")
    train_id = st.number_input("Train ID to Edit", min_value=1, step=1)
    new_name = st.text_input("New Train Name")
    new_type = st.selectbox("New Train Type", ["Express", "Local"])
    new_start = st.text_input("New Start Time")
    new_end = st.text_input("New End Time")

    if st.button("Update"):
        edit_train(train_id, new_name, new_type, new_start, new_end)
        st.success("Train updated successfully!")

# Delete Train Section
if st.sidebar.button("Delete Train"):
    st.header("Delete Train")
    train_id = st.number_input("Train ID to Delete", min_value=1, step=1)
    if st.button("Delete"):
        delete_train(train_id)
        st.success("Train deleted successfully!")
