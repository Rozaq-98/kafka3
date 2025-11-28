from kafka import KafkaProducer
import csv, json, time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

with open('merchants.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        producer.send('merchants', row)
        print("Sent merchant:", row)
        time.sleep(0.5)

producer.flush()
