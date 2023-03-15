import psycopg2
from db_config import config

def create_tables():
    commands = ("""
        CREATE TABLE IF NOT EXISTS car (
            car_id VARCHAR(50) NOT NULL PRIMARY KEY,
            price INT NOT NULL,
            make VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            model_version VARCHAR(100) NOT NULL,
            mileage_in_km INT,
            registration_date DATE ,
            body_type VARCHAR(100) ,
            numberOfSeats INT,
            numberOfDoors INT,
            body_color VARCHAR(100) ,
            power_in_hp INT ,
            transmission VARCHAR(100) ,
            gears INT ,
            rawDisplacementInCCM INT,
            fuel_category VARCHAR(50) ,
            city VARCHAR(100) ,
            street VARCHAR(100) ,
            seller VARCHAR(50),
            created_at DATE  
        )
        """,)

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
