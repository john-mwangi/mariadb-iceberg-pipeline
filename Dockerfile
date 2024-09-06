FROM flink:1.20.0-scala_2.12

USER flink:flink

RUN curl -Lo /opt/flink/lib/flink-sql-connector-mysql-cdc-3.0.1.jar https://repo1.maven.org/maven2/com/ververica/flink-sql-connector-mysql-cdc/3.0.1/flink-sql-connector-mysql-cdc-3.0.1.jar && \
    curl -Lo /opt/flink/lib/flink-shaded-hadoop-2-uber-2.7.5-10.0.jar https://repo.maven.apache.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.7.5-10.0/flink-shaded-hadoop-2-uber-2.7.5-10.0.jar && \
    curl -Lo /opt/flink/lib/iceberg-flink-runtime-1.16-1.3.1.jar https://repo.maven.apache.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.16/1.3.1/iceberg-flink-runtime-1.16-1.3.1.jar