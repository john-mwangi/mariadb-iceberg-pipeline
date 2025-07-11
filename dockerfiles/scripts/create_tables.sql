
-- SHOW VARIABLES LIKE '%log%';
-- SHOW MASTER STATUS;
-- SHOW GLOBAL VARIABLES WHERE variable_name = 'binlog_row_value_options';

-- Set global variables
-- SET @@global.binlog_row_value_options="" ;

-- Create users
CREATE USER 'debezium-user'@localhost IDENTIFIED BY 'debezium-user-pw';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'debezium-user' IDENTIFIED BY 'debezium-user-pw';
FLUSH PRIVILEGES;

-- Create tables
CREATE DATABASE db_1;
 USE db_1;
 CREATE TABLE user_1 (
   id INTEGER NOT NULL PRIMARY KEY,
   name VARCHAR(255) NOT NULL DEFAULT 'flink',
   address VARCHAR(1024),
   phone_number VARCHAR(512),
   email VARCHAR(255)
 );

 INSERT INTO user_1 VALUES (110,"user_110","Shanghai","123567891234","user_110@foo.com");

 CREATE TABLE user_2 (
   id INTEGER NOT NULL PRIMARY KEY,
   name VARCHAR(255) NOT NULL DEFAULT 'flink',
   address VARCHAR(1024),
   phone_number VARCHAR(512),
   email VARCHAR(255)
 );

INSERT INTO user_2 VALUES (120,"user_120","Shanghai","123567891234","user_120@foo.com");


CREATE DATABASE db_2;
USE db_2;
CREATE TABLE user_1 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT 'flink',
  address VARCHAR(1024),
  phone_number VARCHAR(512),
  email VARCHAR(255)
);
INSERT INTO user_1 VALUES (110,"user_110","Shanghai","123567891234", NULL);

CREATE TABLE user_2 (
  id INTEGER NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT 'flink',
  address VARCHAR(1024),
  phone_number VARCHAR(512),
  email VARCHAR(255)
);
INSERT INTO user_2 VALUES (220,"user_220","Shanghai","123567891234","user_220@foo.com");

CREATE DATABASE machine_learning;
USE machine_learning;
CREATE TABLE predictions (
  prediction_id VARCHAR(255) NOT NULL PRIMARY KEY,
  customer_id INTEGER,
  credit_score INTEGER,
  email VARCHAR(255)
);
INSERT INTO predictions VALUES ('d3964613c7c542f2b997a5e76248df3b', 999999, 123, 'example@email.com');