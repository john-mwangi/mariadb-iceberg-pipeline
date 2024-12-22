Spark SQL is the most feature rich compute engine for Iceberg operations. To 
query Iceberg tables using Spark SQL:
1. Define your catalogs before starting a Spark SQL session. The configuration 
in `Dockerfile.sparksql` defines different catalogs: `spark_catalog`, 
`paimon_catalog` and `iceberg_catalog`
1. Start a streaming job. Refer to `create_jobs.sql` to start a `kafka_sync_table` job
1. Start the Spark SQL session: `docker compose run spark-sql`
1. Run the queries in `create_jobs.sql`