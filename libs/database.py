import logging

import psycopg2

import settings
from libs.model import Record

db_conn = None
logger = logging.getLogger(__name__)


def create_table_if_needed():
    """
    Create tables on DB if they don't already exists
    :return:
    """
    conn = db_conn['connection']
    cur = conn.cursor()
    sql_statement = f"CREATE TABLE IF NOT EXISTS {db_conn['schema']}.{db_conn['table']} (" \
                    "id serial PRIMARY KEY," \
                    "url varchar(200) not null," \
                    "start_time timestamp not null," \
                    "access_time decimal not null," \
                    "status_code int," \
                    "regex varchar(200)," \
                    "regex_found boolean);"
    logger.info(cur.mogrify(sql_statement))
    cur.execute(sql_statement)
    logger.info(f"Created table {db_conn['table']} on {db_conn['name']}")
    cur.close()
    conn.commit()


def initialize_connections():
    global db_conn
    for database in settings.DATABASES:
        logger.info(f"Connecting to {database['name']}")
        conn = psycopg2.connect(database=database['database'],
                                user=database['user'],
                                password=database['password'],
                                host=database['host'],
                                port=database['port'])
        db_conn = {
            'name': database['name'],
            'schema': database['schema'],
            'connection': conn,
            'table': database['table']
        }

    logger.info(f'Connected to database')
    create_table_if_needed()


def write_record(record: Record):
    conn = db_conn['connection']
    with db_conn['connection'].cursor() as cur:
        sql_statement = f"INSERT INTO {db_conn['schema']}.{db_conn['table']}" \
                        "(url, start_time, access_time, status_code, regex, regex_found)" \
                        "VALUES (%s, %s ,%s, %s, %s, %s);"
        cur.execute(sql_statement, record.to_tuple())
        cur.close()
        conn.commit()
        logger.info(f"Wrote to {db_conn['name']} record: {record}")


if __name__ == '__main__':
    from datetime import datetime

    initialize_connections()
    write_record(Record('www.google.com', datetime.now(), 1.1, 200, ))
