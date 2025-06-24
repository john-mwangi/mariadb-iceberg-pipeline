## FLINK SQL
Log into Flink SQL terminal.
```shell
docker compose run sql-client
```

Set the execution checkpoint, if not set. This implementation already sets this
in docker compose file.
```sql
SET execution.checkpointing.interval = '3s';
```

Create sources from the DB.
```sql
CREATE TABLE user_source (
    database_name STRING METADATA VIRTUAL,
    table_name STRING METADATA VIRTUAL,
    `id` INTEGER NOT NULL,
    name STRING,
    address STRING,
    phone_number STRING,
    email STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
  ) WITH (
    'connector' = 'mysql-cdc',
    'hostname' = 'mariadb',
    'port' = '3306',
    'username' = 'root',
    'password' = 'mypass',
    'database-name' = 'db_[0-9]+',
    'table-name' = 'user_[0-9]+'
  );
```

Create a sink.
```sql
CREATE TABLE all_users_sink (
    database_name STRING,
    table_name    STRING,
    `id`          INTEGER NOT NULL,
    name          STRING,
    address       STRING,
    phone_number  STRING,
    email         STRING,
    PRIMARY KEY (database_name, table_name, `id`) NOT ENFORCED
  ) WITH (
    'connector'='iceberg',
    'catalog-name'='iceberg_catalog',
    'catalog-type'='hadoop',  
    'warehouse'='file:///tmp/iceberg/warehouse',
    'format-version'='2'
  );
```

Start a streaming job.
```sql
INSERT INTO all_users_sink select * from user_source;
```

Monitor the data lake.
```sql
SELECT * FROM all_users_sink; 
```

## KAFKA SINK
Log into the Flink SQL terminal as described above.

Ensure that the execution checkpoint has been set. This is already done in the
docker compose file for this implementation.

Create sources from Kafka.
```sql
CREATE TABLE user_source_kafka (
    database_name STRING METADATA FROM 'value.source.database' VIRTUAL,
    table_name STRING METADATA FROM 'value.source.table' VIRTUAL,
    topic STRING METADATA FROM 'topic' VIRTUAL,
    `id` INTEGER NOT NULL,
    name STRING,
    address STRING,
    phone_number STRING,
    email STRING,
    PRIMARY KEY (`id`) NOT ENFORCED
  ) WITH (
    'connector' ='kafka',
    -- 'topic' = 'users.db_1.user_1;users.db_1.user_2;users.db_2.user_1;users.db_2.user_2',
    'topic-pattern' = 'users\.db_[0-9]+\.user_[0-9]+',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'debezium-json.schema-include' = 'true'
  );
```

Create a Kafka sink in Iceberg.
```sql
CREATE TABLE all_users_sink_kafka (
  database_name STRING,
  table_name    STRING,
  topic         STRING,
  `id`          INTEGER NOT NULL,
  name          STRING,
  address       STRING,
  phone_number  STRING,
  email         STRING,
  PRIMARY KEY (database_name, table_name, `id`) NOT ENFORCED
) WITH (
    'connector'='iceberg',
    'catalog-name'='iceberg_catalog',
    'catalog-type'='hadoop',
    'warehouse'='file:///tmp/iceberg/warehouse',
    'format-version'='2'
  );
```

Start a streaming job.
```sql
INSERT INTO all_users_sink_kafka SELECT * FROM user_source_kafka;
```

Monitor the table in the data lake.
```sql
-- Results will show in a non-paginated view
-- SET 'sql-client.execution.result-mode' = 'tableau';

SELECT * FROM all_users_sink_kafka;
```

**If using the `machine_learning` database**
Create sources from Kafka.
```sql
CREATE TABLE ml_source_kafka (
    database_name STRING METADATA FROM 'value.source.database' VIRTUAL,
    table_name STRING METADATA FROM 'value.source.table' VIRTUAL,
    topic STRING METADATA FROM 'topic' VIRTUAL,
    prediction_id STRING NOT NULL,
    customer_id INTEGER,
    credit_score INTEGER,
    email STRING,
    PRIMARY KEY (prediction_id) NOT ENFORCED
  ) WITH (
    'connector' ='kafka',
    'topic' = 'users.machine_learning.predictions',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'debezium-json.schema-include' = 'true'
  );
```

Create a Kafka sink in Iceberg.
```sql
CREATE TABLE ml_sink_kafka (
  database_name STRING,
  table_name    STRING,
  topic         STRING,
  prediction_id STRING,
  customer_id   INTEGER,
  credit_score  INTEGER,
  email         STRING,
  PRIMARY KEY (database_name, table_name, prediction_id) NOT ENFORCED
) WITH (
    'connector'='iceberg',
    'catalog-name'='iceberg_catalog',
    'catalog-type'='hadoop',
    'warehouse'='file:///tmp/iceberg/warehouse',
    'format-version'='2'
  );
```

Start a streaming job.
```sql
INSERT INTO ml_sink_kafka SELECT * FROM ml_source_kafka;
```

Monitor the table in the data lake.
```sql
-- Results will show in a non-paginated view
SET 'sql-client.execution.result-mode' = 'tableau';

SELECT * FROM ml_sink_kafka;
```

## PAIMON KAFKA TABLE SYNC ACTION
Log into the Flink SQL terminal.

Create a Paimon catalog using Flink SQL.
```sql
CREATE CATALOG paimon_catalog WITH (
    'type' = 'paimon',
    'warehouse' = 'file:///tmp/paimon/warehouse'
);
```

Log into the jobmanager container.
```bash
docker exec -ti jobmanager bash
```

Synchronisation of one Paimon table to one Kafka topic.
```bash
flink run \
    /opt/flink/lib/paimon-flink-action-1.0.0.jar \
    kafka_sync_table \
    --warehouse file:///tmp/paimon/warehouse \
    --database users_ta \
    --table user_2 \
    --primary_keys id \
    --kafka_conf properties.bootstrap.servers=kafka:9092 \
    --kafka_conf topic=users.db_1.user_2 \
    --kafka_conf value.format=debezium-json \
    --table_conf changelog-producer=input \
    --kafka_conf scan.startup.mode=earliest-offset
```

Select from the newly synced table.
```sql
SELECT * FROM paimon_catalog.users_ta.user_2;
```

## PAIMON KAFKA DB SYNC ACTION
Create paimon_catalog as described above.

Log in to the jobmanager container as described above.

Synchronization from multiple Kafka topics to a Paimon database.
```bash
flink run \
    /opt/flink/lib/paimon-flink-action-1.0.0.jar \
    kafka_sync_database \
    --warehouse file:///tmp/paimon/warehouse \
    --database users_da \
    --primary_keys id \
    --kafka_conf properties.bootstrap.servers=kafka:9092 \
    --kafka_conf topic-pattern=users\.db_[0-9]+\.user_[0-9]+ \
    --kafka_conf value.format=debezium-json \
    --table_conf changelog-producer=input \
    --kafka_conf scan.startup.mode=earliest-offset \
    --table_conf bucket=4 \
    --table_conf auto-create=false
```

This action will create one database (users_da) with 2 tables:
- user_1 (merging all tables called user_1)
- user_2 (merging all tables called user_2)

Investigate synced tables in Paimon.
```sql
SHOW DATABASES IN paimon_catalog;
SHOW TABLES IN paimon_catalog.users_da;
SELECT * FROM paimon_catalog.users_da.user_1;
SELECT * FROM paimon_catalog.users_da.user_2;
```

## PAIMON ICEBERG COMPATIBILITY
Create paimon_catalog as described above.

Create an Iceberg catalog.
```sql
CREATE CATALOG iceberg_catalog WITH (
    'type' = 'iceberg',
    'catalog-type' = 'hadoop',
    'warehouse' = 'file:///tmp/paimon/warehouse/iceberg',
    'cache-enabled' = 'false' -- disable iceberg catalog caching to quickly see the result
);
```

Log into the jobmanager container.

Create a kafka_sync_table job.
```bash
flink run \
    /opt/flink/lib/paimon-flink-action-1.0.0.jar \
    kafka_sync_table \
    --warehouse file:///tmp/paimon/warehouse \
    --database users_ta_ice \
    --table user_2 \
    --primary_keys id \
    --kafka_conf properties.bootstrap.servers=kafka:9092 \
    --kafka_conf topic=users.db_1.user_2 \
    --kafka_conf value.format=debezium-json \
    --table_conf changelog-producer=input \
    --kafka_conf scan.startup.mode=earliest-offset \
    --table_conf metadata.iceberg.storage=hadoop-catalog
```

Investigate the synced table for compatibility.
```sql
SHOW DATABASES IN paimon_catalog;
SHOW TABLES IN paimon_catalog.users_ta_ice;
SHOW DATABASES IN iceberg_catalog;
SHOW TABLES IN iceberg_catalog.users_ta_ice;
DESCRIBE iceberg_catalog.users_ta_ice.user_2;
SELECT * FROM iceberg_catalog.users_ta_ice.user_2;
```

## SPARK SQL

Run kafka_sync_table.

Access Spark SQL.
```bash
docker compose run spark-sql
```

Query some tables in using Spark.
```sql
DESCRIBE iceberg_catalog.`users_ta_ice.db`.user_2;
DESCRIBE paimon_catalog.users_ta_ice.user_2;
```