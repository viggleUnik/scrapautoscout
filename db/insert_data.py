from typing import Dict
import psycopg2
from db.db_config import config
import logging
import os

log = logging.getLogger(os.path.basename(__file__))


def insert_into_car_table(data: Dict, db_params: Dict = None):

    fields = list(data.keys())
    values = list(data.values())

    # Construct the SQL statement dynamically
    sql = "INSERT INTO car ({}) VALUES ({}) ON CONFLICT DO NOTHING".format(
        ', '.join(fields),
        ', '.join(['%s'] * len(fields))
    )

    conn = None
    try:
        if db_params is None:
            # read the connection parameters
            params = config()
        else:
            params = db_params

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, values)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        count = cur.rowcount
        log.info(f' {count}, Record inserted successfully into car table')
    except (Exception, psycopg2.DatabaseError) as error:
        log.error(f'ERROR: {error}')
    finally:
        if conn is not None:
            conn.close()
