from typing import Dict
import psycopg2
from db.db_config import config
import logging
import os

log = logging.getLogger(os.path.basename(__file__))

def insert_into_car_table(data: Dict):
    # insert query with check if record doesn't already exist
    insert_query = """ INSERT INTO car( car_id,
                                        price,
                                        make,
                                        model,
                                        model_version,
                                        mileage_in_km,
                                        registration_date,
                                        body_type,
                                        numberOfSeats,
                                        numberOfDoors,
                                        body_color,
                                        power_in_hp,
                                        transmission,
                                        gears,
                                        rawDisplacementInCCM,
                                        fuel_category,
                                        city,
                                        street,
                                        seller,
                                        created_at)
        VALUES (%s, %s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s, %s,%s, CURRENT_DATE) 
        ON CONFLICT DO NOTHING
    """
    record_to_insert = (
        data['car_id'], int(data['price']), data['make'], data['model'], data['model_version'],
        int(data['mileage_in_km']), data['registration_date'], data['body_type'],
        int(data['numberOfSeats']), int(data['numberOfDoors']), data['body_color'],
        int(data['power_in_hp']), data['transmission'], data['gears'], int(data['rawDisplacementInCCM']),
        data['fuel_category'], data['city'], data['street'], data['seller'])

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(insert_query, record_to_insert)
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
