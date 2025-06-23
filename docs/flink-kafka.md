# About
This implements the a streaming pipeline from Maria DB to Iceberg with Kafka as the message broker.
It uses Flink SQL instead of Kafka Connect to connect Kafka to Iceberg.

# Implementation
1. Create Docker services
1. Access Kafka UI to monitor Kafka message
1. Access Flink Jobmanager dashboard to monitor streaming jobs
1. Access Flink SQL terminal: `docker compose -f docker-compose-demo.yml run --remove-orphans sql-client`

# Operation
The following operations are perform on the Flink SQL terminal to demostrate the functionality of the streaming pipeline.
1. Create streaming job: Run commands in `scripts/create_jobs.sql`
1. Monitor data warehouse contents: Use the command in `scripts/create_jobs.sql`
1. Perform CRUD operations in Maria DB: Run commands in `scripts/run_crud.sql`
1. Accessing Maria DB:
```bash
docker exec -ti mariadb bash
mariadb -uroot -pmypass
```