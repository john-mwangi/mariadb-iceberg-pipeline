"""This module creates dummy messages of prediction events from an ML model"""

import random
from uuid import uuid4
from time import sleep
from kafka import KafkaProducer
import json
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Table, MetaData, insert

env_path = "/home/john/mariadb-iceberg-pipeline/dockerfiles/scripts/.env"
load_dotenv(env_path)

PREDICTIONS_TOPIC = "prediction_details"
KAFKA_SERVER = "localhost:29092"
ALERTS_EMAIL = os.environ.get("ALERTS_EMAIL")

def send_to_topic():
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    for i in range(10):
        prediction_id = uuid4().hex
        prediction = {
                "prediction_id": prediction_id,
                "customer_id": i + 1,
                "credit_score": random.randint(0,1000),
                "email": ALERTS_EMAIL
            }

        producer.send(
            topic=PREDICTIONS_TOPIC,
            value=json.dumps(prediction).encode("utf-8")
        )
        
        print(f"Successfully sent {prediction_id=} to topic: '{PREDICTIONS_TOPIC}'")
        sleep(2)
        
def send_to_db():
    user = os.environ.get("MARIADB_ROOT_USERNAME")
    password = os.environ.get("MARIADB_DEMO_PASSWORD")
    host = os.environ.get("MARIADB_HOST")
    port = os.environ.get("MARIADB_PORT")
    db = os.environ.get("ML_DATABASE")
    dialect = os.environ.get("DATABASE_DIALECT")
    connector = os.environ.get("DATABASE_CONNECTOR")
    table_name = os.environ.get("ML_TABLE")
    
    db_url = f"{dialect}+{connector}://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(db_url)
    table = Table(table_name, MetaData(), autoload_with=engine)
    
    for i in range(10):
        prediction_id = uuid4().hex
        prediction = {
                "prediction_id": prediction_id,
                "customer_id": i + 1,
                "credit_score": random.randint(0,1000),
                "email": ALERTS_EMAIL
            }
        
        stmt = insert(table=table).values(**prediction)
        with engine.begin() as conn:
            conn.execute(stmt)
        
        print(f"Successfully saved {prediction_id=} to {table_name=}")
        sleep(2)

if __name__ == "__main__":
    send_to_db()