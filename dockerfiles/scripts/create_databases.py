"""This script creates replicas of the MediaWiki database"""

import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine, insert, inspect, text, select
from sqlalchemy.exc import ProgrammingError

load_dotenv()

user = os.environ.get("MARIADB_ROOT_USERNAME")
password = os.environ.get("MARIADB_ROOT_PASSWORD")
host = os.environ.get("MARIADB_HOST")
port = os.environ.get("MARIADB_PORT")
db = os.environ.get("MARIADB_DATABASE")
dialect = os.environ.get("DATABASE_DIALECT")
connector = os.environ.get("DATABASE_CONNECTOR")

def create_databases(n=2) -> list[str]:
    """Creates a copy of a database.

    Args
    ---
    n: Number of database copies to create

    Returns
    ---
    list of databases created
    """

    engine = create_engine(f"{dialect}+{connector}://{user}:{password}@{host}:{port}")

    databases = []

    for i in range(n):
        db_name = f"{db}_{i}"
        query = text(f"CREATE DATABASE {db_name};")

        autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")

        try:
            with autocommit_engine.begin() as conn:
                conn.execute(query)

            print(f"successfully created database {db_name}")

        except ProgrammingError:
            print(f"database {db_name} already exists")

        databases.append(db_name.lower())

    return databases


def create_tables(dbs: list[str]) -> None:
    """Copies the tables of a reference database to another database

    Args
    ---
    * dbs: the databases to copy data to
    """

    engine = create_engine(f"{dialect}+{connector}://{user}:{password}@{host}:{port}/{db}")
    db_inspector = inspect(engine)
    tables = db_inspector.get_table_names()
    print(f"tables in {db}: {tables}")

    for d in dbs:

        eng = create_engine(f"{dialect}+{connector}://{user}:{password}@{host}:{port}/{d}")

        # create tables
        for tbl in tables:
            metadata = MetaData()
            ref_table = Table(tbl, metadata, autoload_with=engine)
            schema = ref_table.columns.items()
            print(f"schema for {ref_table} in {db}: {schema}\n")

            metadata.create_all(eng)
            print(f"successfully created '{tbl}' in '{d}'\n")

        # populate tables
        for tbl in tables:
            source = Table(tbl, MetaData(), autoload_with=engine)
            query = select(source)
            
            with engine.connect() as conn:
                data = conn.execute(query).fetchall()

            destination = Table(tbl, MetaData(), autoload_with=eng)

            with eng.begin() as conn:
                if data:
                    conn.execute(insert(destination), [r._mapping for r in data])

            print(f"successfully copied data to '{tbl}' in '{d}'\n")


def main():
    databases = create_databases(n=5)
    create_tables(dbs=databases)


if __name__ == "__main__":
    main()
