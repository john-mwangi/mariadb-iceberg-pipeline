# Solution Architecture

Below is the overall architecture of this event-driven, CDC-based, streaming 
data pipeline.

```mermaid
%% Solution Architecture Diagram
graph TD
    subgraph "Database"
        A[("MariaDB")]
    end

    subgraph "Change Data Capture"
        B[/"Debezium"/]
    end

    subgraph "Message Broker"
        C[/"Apache Kafka"/]
    end

    subgraph "Flink SQL"
        D["ml_source table"]
        E["ml_sink table"]
    end

    subgraph "Data Lake"
        F[("Apache Iceberg")]
    end

    subgraph "Dashboard"
        G[/"Apache Flink"/]
    end

    subgraph "Querying"
        H[/"Spark SQL"/]
    end

    A --"Database Operations"--> B
    B --"Event Stream"--> C
    C --"sources"--> D
    D --"sink"--> E
    E --"Streaming Pipeline"--> F
    F --"User Queries" --> H
    E --"Job Monitoring" --> G
```

# Feature Design

Below is a sequence diagram for the feature that is going to be implemented.

```mermaid
%% Feature Design
sequenceDiagram
    participant ML_Service as ML Model
    participant Kafka as Kafka
    participant Validator_App as Validator App
    participant Alerts_App as Alerts App
    participant Advisor as Customer Advisor

    ML_Service->>Kafka: Writes prediction_details topic
    Kafka-->>Validator_App: Reads prediction_details topic
    Validator_App->>Validator_App: Validates credit_score
    Validator_App->>Kafka: Writes qualified_leads topic (if validation passes)
    Kafka-->>Alerts_App: Reads qualified_leads topic
    Alerts_App->>Advisor: Sends success alerts
```
