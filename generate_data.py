from faker import Faker
import pymysql
import random
from datetime import datetime
import streamlit as st

fake = Faker()

conn = pymysql.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"],
    port=st.secrets["mysql"]["port"]
)
cursor = conn.cursor()

NUM_CUSTOMERS = 500

# --- 1. Customers ---
for i in range(1, NUM_CUSTOMERS + 1):
    name = fake.name()
    age = random.randint(18, 60)
    signup_date = fake.date_between(start_date='-3y', end_date='today')
    is_churned = random.choice([0, 1])
    cursor.execute("""
        INSERT INTO customers (customer_id, name, age, signup_date, is_churned)
        VALUES (%s, %s, %s, %s, %s)
    """, (i, name, age, signup_date, is_churned))

# --- 2. Services ---
service_types = ['Internet', 'Mobile', 'TV', 'Cloud', 'Banking']
for i in range(1, NUM_CUSTOMERS + 1):
    service_type = random.choice(service_types)
    start_date = fake.date_between(start_date='-3y', end_date='today')
    cursor.execute("""
        INSERT INTO services (customer_id, service_type, start_date)
        VALUES (%s, %s, %s)
    """, (i, service_type, start_date))

# --- 3. Complaints ---
complaint_types = ['Billing', 'Network', 'Support', 'Service', 'App']
for _ in range(NUM_CUSTOMERS):  
    cust_id = random.randint(1, NUM_CUSTOMERS)
    complaint_type = random.choice(complaint_types)
    complaint_date = fake.date_between(start_date='-2y', end_date='today')
    cursor.execute("""
        INSERT INTO complaints (customer_id, complaint_type, complaint_date)
        VALUES (%s, %s, %s)
    """, (cust_id, complaint_type, complaint_date))

# --- 4. Feedbacks ---
for i in range(1, NUM_CUSTOMERS + 1):
    rating = str(random.randint(1, 5))
    cursor.execute("""
        INSERT INTO feedbacks (customer_id, feedback_rating)
        VALUES (%s, %s)
    """, (i, rating))

# --- 5. Usage ---
for i in range(1, NUM_CUSTOMERS + 1):
        month = random.randint(1,12) # last 3 months usage
        usage_minutes = random.randint(300, 1500)
        cursor.execute("""
            INSERT INTO usages (customer_id, usage_month, usage_minutes)
            VALUES (%s, %s, %s)
        """, (i, month, usage_minutes))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Faker data inserted successfully!")
