## Goals & Objectives
The over-arching goal of the assignment was to determine if the possiblility of
having incremental updates of MediaWiki data in the data lake, using Change 
Data Capture (CDC). To accomplish this, we conducted an experiment to 
investigate the following capabilities:

**Capability** | **Supported**
--- | ---
Initiating a streaming job directly from a MariaDB database to an Iceberg data lake | Yes
Using Kafka as a sink and establishing a streaming job from Kafka to Iceberg | Yes
Implement automated schema evolution between MariaDB and Paimon data lake in a streaming job | Yes
Implement compatibility between Paimon and Iceberg data lakes | Yes
Querying Paimon & Iceberg data lakes using Spark SQL and Flink SQL | Yes

## Solution Design
(mermaid diagram)

**Component** | **Use / Rationale**
--- | ---
MariaDB | MediaWiki database is on MariaDB
Debezium CDC | Flink CDC does not capture the "schema" field which is required for schema evolution support
Kafka | Message broker
Flink SQL | Default interface for creating streaming jobs and querying tables
Spark SQL | Alternative interface for querying tables
Kafka UI | Dashboard for viewing Kafka messages or manually creating them
Flink UI | Dashboard for monitoring streaming jobs
Iceberg | The data lake
Paimon | An alternative data lake to Iceberg with support for schema evolution and compatible with Iceberg

## Outcomes & Observations
With reference to the plan outlined in the *Implementation Process* section of 
the README, all the capabilities were implemented and are supported.

Once initiated, the streaming jobs can be monitored in the Flink UI dashboard
while the Kafka messages can be monitored on the Kafka UI dashboard. The tables
can be queried using either Spark or Flink SQL.

Schema evolution between source and destination tables is automatically handled 
by the Paimon Kafka sync jobs between MariaDB and Paimon data lake. This 
includes: adding/removal of tables, adding/removal of columns, renaming of 
columns, type changes (except type widening). With Paimon v1.0, it is now 
possible to access Paimon tables from Iceberg via the Iceberg Compatability 
Mode. See `./docs/schema-evolution.md` for further details.

## Conclusions
* The pipeline is able to support incremental updates from MediaWiki.
* Because schema evolution is currently only supported in Paimon, while
being accessible from Iceberg, the cost implications of supporting 2 data lakes
consurrently should be carefully considered. According to the current Iceberg 
product roadmap, this functionality is planned for XXX.