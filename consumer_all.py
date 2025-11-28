from kafka import KafkaConsumer
import pyodbc
import json

# SQL SERVER CONNECTION
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-FQEG6UP1\SQLEXPRESS;'
    'DATABASE=TestDB;'   # ganti sesuai database Anda
    'UID=sa;'            # user
    'PWD=Rozaq123;'  # password
)
cursor = conn.cursor()

# Kafka consumer multi-topic
consumer = KafkaConsumer(
    'users', 'merchants', 'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print("Consumer running...")

for msg in consumer:
    data = msg.value
    topic = msg.topic

    print(f"Received from {topic}: {data}")

    if topic == "users":
        cursor.execute("""
            INSERT INTO users (user_id, user_name, signup_date)
            VALUES (?, ?, ?)
        """, (data["user_id"], data["user_name"], data["signup_date"]))

    elif topic == "merchants":
        cursor.execute("""
            INSERT INTO merchants (merchant_id, merchant_name, merchant_category)
            VALUES (?, ?, ?)
        """, (data["merchant_id"], data["merchant_name"], data["merchant_category"]))

    elif topic == "transactions":
        cursor.execute("""
            INSERT INTO transactions (transaction_id, user_id, merchant_id, amount, transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["transaction_id"], data["user_id"], data["merchant_id"],
            data["amount"], data["transaction_date"]
        ))

    conn.commit()
    print("Inserted into SQL Server")
