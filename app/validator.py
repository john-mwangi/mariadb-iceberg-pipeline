"""This module simulates an app that evaluates whether a customer qualifies for a 
loan based on their credit score"""

from ml_model import PREDICTIONS_TOPIC, KAFKA_SERVER
from kafka import KafkaConsumer, KafkaProducer
import json

QUALIFIED_LEADS_TOPIC = "qualified_leads"
MIN_CREDIT_SCORE = 500

consumer = KafkaConsumer(topic=PREDICTIONS_TOPIC, bootstrap_servers=KAFKA_SERVER)
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

while True:
    for msg in consumer:
        prediction = json.loads(msg.value.decode())
        print(f"Read message: {prediction=}")
        
        credit_score = prediction["credit_score"]
        customer_id = prediction["customer_id"]
        
        if credit_score > MIN_CREDIT_SCORE:
            producer.send(
                topic=QUALIFIED_LEADS_TOPIC,
                value=json.dumps(prediction).encode("utf-8")
            )
            print(f"Qualified lead: {customer_id}")