import pyodbc
import pandas as pd

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-FQEG6UP1\SQLEXPRESS;'
    'DATABASE=TestDB;'   # ganti sesuai database Anda
    'UID=sa;'            # user
    'PWD=Rozaq123;'  # password
)

print("\n=== Total Amount per User per Day ===")
df1 = pd.read_sql("""
    SELECT user_id, transaction_date, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY user_id, transaction_date
    ORDER BY transaction_date, user_id
""", conn)
print(df1)

print("\n=== Total Transactions per Merchant ===")
df2 = pd.read_sql("""
    SELECT merchant_id, COUNT(*) AS total_tx, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY merchant_id
    ORDER BY total_tx DESC
""", conn)
print(df2)
