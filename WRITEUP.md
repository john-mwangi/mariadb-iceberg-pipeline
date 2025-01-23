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

**Component** | **Use / Rationale**
--- | ---
MariaDB | MediaWiki database is on MariaDB
Debezium CDC | Flink CDC does not capture the "schema" field which is required for schema evolution support
Kafka | Message broker
Flink SQL | Default interface for creating streaming jobs and querying tables
Spark SQL | Alternative Spark interface for querying tables
Kafka UI | Dashboard for viewing Kafka messages or manually creating them
Flink UI | Dashboard for monitoring streaming jobs

## Outcomes & Observations
With reference to the detailed tasks outlined in the *Implementation Process* 
section of the README, all the capabilities were implemented except for the Paimon
Iceberg Compatibility which has been partially implemented in Paimon v0.9 but
is expected to be fully implemented in Paimon v1.0.

Once initiated, the streaming jobs can be monitored in the Flink UI dashboard
while the Kafka messages can be monitored on the Kafka UI dashboard. The tables
can be queried using either Spark or Flink SQL.

Schema evolution between source and destination tables is automatically handled 
by the Paimon Kafka sync jobs between MariaDB and Paimon data lake. This includes: adding/removal of tables, adding/removal of columns, renaming of columns, type 
changes (except type widening). As mentioned above, it is currently not possible 
to access Paimon tables from Iceberg as the Iceberg Compatability Mode is WIP.
See `./docs/schema-evolution.md` for further details.

## Conclusions
* The pipeline is able to support incremental updates from MediaWiki.
* Whereas schema evolution is working, it should not be implemented until the 
Iceberg Compatibility Mode is fully functional.
* Iceberg Compatibilty Mode should be retested when Paimon v1.0 is released 
(ongoing).