# Mariadb-Iceberg Pipeline
## Objectives
Determine the feasibility of:
* Maintaining incrementally updated and queryable MediaWiki MariaDB tables in the Data Lake
* Generating state change events in Kafka from MediaWiki MariaDB
* Document learnings along the way

## Implementation pattern
1. **Flink SQL:** Mariadb -> Flink SQL -> Iceberg
1. **Flink CDC:** Mariadb -> Flink CDC -> Kafka -> Iceberg
1. **Debezium CDC:** Mariadb -> Debezium -> Kafka -> Iceberg

## Set up
### 1. Build the services
Running this docker-compose file will download the necessary connectors and place them
in the correct directories.
```
docker compose -f docker-compose-demo.yml up --build --remove-orphans -d
```

>[!TIP]
> Use `dockerfiles/versions.env` to upgrade components of the pipeline.

### 2. Create a streaming job
Refer to `./docs`

### 3. Monitor streaming jobs
- Flink UI: http://localhost:8081/
- Kafka UI: http://localhost:8082/ (u: admin, p:admin)
- MediaWiki UI: http://localhost:8083/wiki/Main_Page

## Implementation process
Below is the implementation procedure that will be followed, to be updated as necessary:
- [x] Install required services
    - [x] Install Apache Iceberg with Spark
    - [x] Install MariaDB
    - [x] Install Apache Flink
    - [x] Install Apache Kafka
- [x] Create a streaming Flink SQL job
    - [x] Create physical tables in Maria DB
    - [x] Create source table in Iceberg
    - [x] Create sink table in Iceberg (Hadoop catalog type)
    - [x] Create Flink SQL streaming job
    - [x] Test streaming job
    - [x] Create automation scripts
- [ ] Create a streaming Flink CDC Kafka job <sup>[1]</sup>
    - [ ] Downgrade to [Flink 1.17](https://nightlies.apache.org/flink/flink-cdc-docs-master/docs/connectors/flink-sources/overview/#supported-flink-versions)
    - [ ] Test Kafka: create a test topic and manually publish a message to it
    - [ ] Create a destination table in Iceberg (test_table_flink)
    - [ ] Test Kafka -> Iceberg: configure Kafka to deliver messages to destination table in Iceberg from our test topic in Kafka
    - [ ] Configure Flink with source (Mariadb database) and sink (Kafka test topic)
    - [ ] Create automation scripts
- [x] Create streaming job using Debezium
    - [x] Prepare an implementation guide doc
    - [x] Create services
    - [x] Source (db) configuration
    - [x] Add Kafka UI
    - [x] Connector configuration
        - [x] Source (Maria db)
        - [x] Sink (Kafka)
        - [x] Destination (Iceberg)
    - [x] Test streaming job
- [x] Paimon
    - [x] Research
    - [x] Add paimon catalog with Kafka as sink
    - [x] Test streaming job
    - [x] Implement schema evolution support (Paimon Kafka Sync Action)
    - [x] Test schema evolution
    - [x] Implement Iceberg compatibility
    - [x] Test Iceberg compatibility
- [x] Spark SQL
    - [x] Add Spark SQL
    - [x] Query Iceberg catalog table using Spark SQL
    - [x] Query Paimon catalog table using Spark SQL
- [ ] CDC experimentation
    - [ ] Connect to Analytics/Wiki Replicas <sup>[2]</sup>
    - [x] Install MediaWiki locally
    - [x] Connect to MediWiki db
    - [x] Replace mariadb:11 image with bitnami/mariadb:11.4
    - [x] Add Makefile to rebuilt MediaWiki
    - [x] Update docker-compose.override.yml
        - [x] Add MediakWiki
      	- [x] Add Flink services
	- [x] Add Debezium, Kafka, and related services
    	- [x] Create kafka_database_sync job
    - [ ] Experimentation

> [!NOTE]
> 1. Current Flink CDC version doesn't capture the schema. This is planned for 
[Flink CDC v3.3](https://issues.apache.org/jira/browse/FLINK-36611)
> 2. Analytics Replicas contain unredacted personal user data. Wiki Replicas do not have binlog settings enabled

## Relevant links
* https://phabricator.wikimedia.org/T370354
* https://iceberg.apache.org/spark-quickstart/#docker-compose
* https://github.com/tabular-io/docker-spark-iceberg
* https://mariadb.com/kb/en/installing-and-using-mariadb-via-docker/
* https://nightlies.apache.org/flink/flink-docs-master/docs/deployment/resource-providers/standalone/docker/
* https://hub.docker.com/r/apache/kafka
