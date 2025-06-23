"""This module simulates an app that evaluates whether a customer qualifies for a 
loan based on their credit score"""

from ml_model import PREDICTIONS_TOPIC, KAFKA_SERVER
from kafka import KafkaConsumer, KafkaProducer
import json

QUALIFIED_LEADS_TOPIC = "qualified_leads"
MIN_CREDIT_SCORE = 500

def main():
    consumer = KafkaConsumer(PREDICTIONS_TOPIC, bootstrap_servers=KAFKA_SERVER)
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    print(f"Validator is listening to topic: {PREDICTIONS_TOPIC}")

    counter = 0
    while True:
        for msg in consumer:
            prediction = json.loads(msg.value.decode())    
            credit_score = prediction["credit_score"]
            prediction_id = prediction["prediction_id"]
            counter += 1
            print(f"Messages read: {counter}") 
            
            if credit_score > MIN_CREDIT_SCORE:
                producer.send(
                    topic=QUALIFIED_LEADS_TOPIC,
                    value=json.dumps(prediction).encode("utf-8")
                )
                print(f"Sent Qualified Lead: {prediction_id=}, {credit_score=} to topic: {QUALIFIED_LEADS_TOPIC}")
                
if __name__ == "__main__":
    main()