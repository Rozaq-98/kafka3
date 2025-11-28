from kafka import KafkaProducer
import csv, json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open('transactions.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        producer.send('transactions', row)
        print("Sent transaction:", row)
        time.sleep(0.5)

producer.flush()
