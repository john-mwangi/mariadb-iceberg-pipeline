## Goals & Objectives
The over-arching goal of the assignment was to determine if the possiblility of
having incremental updates of MediaWiki data in the data lake, using Change Data Capture (CDC). To accomplish this, we conducted an experiment to investigate 
the following capabilities:
1. Initiating a streaming job directly from a MariaDB database to an Iceberg data lake.
1. Using Kafka as a sink and establishing a streaming job from Kafka to Iceberg.
1. Implement automated schema evolution between MariDB and Paimon data lake in a streaming job.
1. Implement compatibility between Paimon and Iceberg data lakes.
1. Querying the data lakes using Spark SQL and Flink SQL.

## Solution Design
(mermaid diagram)

## Outcomes
(monitoring, UI, checklist, answers to qs, capabilities, features, etc)

With reference to the detailed tasks outlined in the *Implementation Process* 
section of the README, all the capabilities were implemented except for the Paimon
Iceberg Compatibility which has been partially implemented in Paimon v0.9 but
is expected to be fully implemented in Paimon v1.0.

Once initiated, the streaming jobs can be monitored in the Flink UI dashboard
while the Kafka messages can be monitored on the Kafka UI dashboard. The tables
can be queried using either Spark or Flink SQL.

## FAQs
1. Why Debezium CDC over Flink CDC?

## Outcomes
Notes & observations (missing features)
Answers to questions
Implementation