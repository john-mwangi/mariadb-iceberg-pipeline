"""This module creates dummy messages of prediction events from an ML model"""

import random
from uuid import uuid4
from time import sleep
from kafka import KafkaProducer
import json

PREDICTIONS_TOPIC = "prediction_details"
KAFKA_SERVER = "localhost:29092"

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

for i in range(10):
    prediction_id = uuid4().hex
    prediction = {
            "prediction_id": prediction_id,
            "customer_id": i + 1,
            "credit_score": random.randint(0,1000),
        }

    producer.send(
        topic=PREDICTIONS_TOPIC,
        value=json.dumps(prediction).encode("utf-8")
    )
    
    print(f"Successfully sent {prediction_id=} to topic: '{PREDICTIONS_TOPIC}'")
    sleep(2)
    