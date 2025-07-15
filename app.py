import streamlit as st
import pickle
import pandas as pd
import numpy as np
import mysql.connector, pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="", db="churn_analysis",port =3306)
cursor = conn.cursor()

query_title = []
queries = []
st.title("User Churn Monitoring And Prediction System")
with open("churn_reports.sql", "r") as file:
    raw_sql = file.read()

# Split at each comment, which marks the start of a query
raw_blocks = raw_sql.strip().split("--")

for block in raw_blocks:
    block = block.strip()
    if not block:
        continue

    lines = block.splitlines()
    title = lines[0].strip()  # first line = title
    sql_body = "\n".join(lines[1:]).strip()

    # Only add if there's a valid SQL ending with a semicolon
    if sql_body.endswith(";"):
        query_title.append(title)
        queries.append(sql_body)

# Streamlit UI
selected_query = st.multiselect("Select a query to run", query_title)

for title in selected_query:
    index = query_title.index(title)
    sql = queries[index]

    st.subheader(title)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error executing query '{title}': {e}")


pipe = pickle.load(open("churn_prediction.pkl", "rb"))


st.title("Churn Prediction")
service_type = st.selectbox(
    "Enter service type", ["Internet", "Mobile", "TV", "Cloud", "Banking"]
)
complaint_type = st.selectbox(
    "Enter complaint type", ["Billing", "Network", "Support", "Service", "App"]
)
feedback_rating = st.slider("Enter feedback rating", 0, 5, 2)
usage_month = st.number_input(
    "Enter usage months", min_value=0, max_value=12, step=1, value=5
)
usage_minutes = st.number_input("Enter usage minutes", min_value=0, step=10, value=500)

test_input = pd.DataFrame(
    {
        "service_type": [service_type],
        "feedback_rating": [feedback_rating],
        "complaint_type": [complaint_type],
        "usage_month": [usage_month],
        "usage_minutes": [usage_minutes],
    }
)

result = pipe.predict(test_input)[0]

if st.button("Predict Churn"):
    if result == 0:
        st.error("Customer will leave")
    else:
        st.success("Customer will stay")
    
