import psycopg2
from db_config import config

def create_tables():
    commands = ("""
        CREATE TABLE IF NOT EXISTS car (    
            id VARCHAR(50) NOT NULL PRIMARY KEY,
            vin VARCHAR(50),
            price INT,
            price_currency VARCHAR(10),
            price_negotiable bool,
            price_tax_deductible bool,
            price_net INT,
            vat_rate VARCHAR(50),
            make VARCHAR(100),
            model VARCHAR(100),
            model_version VARCHAR(100),
            german_hsn_tsn VARCHAR(50),
            mileage_km INT,
            production_year INT,
            registration_date DATE,
            vehicle_type VARCHAR(50),
            body_type VARCHAR,
            nr_seats INT ,
            nr_doors INT,
            body_color VARCHAR(50),
            paint_type VARCHAR(50),
            body_color_original VARCHAR(50),
            upholstery VARCHAR(50),
            upholstery_color VARCHAR(50),
            power_hp INT,
            power_kw INT,
            transmission VARCHAR(50),
            gears INT,
            cylinders INT,
            drive_train VARCHAR(50),
            volume_ccm INT,
            weight_kg VARCHAR(50),
            fuel_category VARCHAR(50),
            primary_fuel VARCHAR(50),
            fuel_cons_comb_l100km VARCHAR(50),
            fuel_cons_city_l100km real,
            fuel_cons_highway_l100km  real,
            co2_emission_grperkm INT,
            has_particle_filter bool,
            electric_range_km VARCHAR(50),
            feats_cruise_control INT,
            feats_start_stop INT,
            feats_electrical_side_mirrors INT,
            feats_electrical_adj_seats INT,
            feats_headsup_disp INT,
            feats_panorama_roof INT,
            feats_auto_climate_control INT,
            feats_seats_leather INT,
            feats_seats_massage INT,
            feats_seats_ventilation INT,
            feats_seats_heating INT,
            feats_light_sensor INT,
            feats_navigation INT,
            feats_pdc INT,
            feats_park_sens_front INT ,
            feats_park_sens_rear INT,
            feats_park_camera INT,
            feats_power_windows INT,
            feats_bluetooth INT,
            feats_onboard_computer INT,
            feats_usb INT,
            feats_wifi INT,
            feats_sound INT,
            feats_abs INT,
            feats_adapt_cruise_control INT,
            feats_alarm INT,
            feats_central_lock_remote INT,
            feats_dist_warn_sys INT,
            feats_emergency_brake_assist INT,
            feats_lane_depart_warn_sys INT,
            feats_immobilizer INT,
            feats_tire_monitor INT,
            feats_traction_control INT,
            feats_adapt_headlights INT,
            feats_xenon INT,
            feats_laser INT,
            feats_led INT,
            envir_standard VARCHAR(50),
            original_market VARCHAR(50),
            offer_type VARCHAR(10) ,
            is_used INT,
            is_new INT,
            is_preregistered INT,
            had_accident bool,
            has_full_service_history bool,
            non_smoking bool,
            nr_prev_owners INT,
            is_rental bool,
            country_code VARCHAR(10),
            zip VARCHAR(20),
            city VARCHAR(50),
            street VARCHAR(50),
            latitude real,
            longitude real,
            seller_is_dealer bool,
            seller_type VARCHAR(30),
            seller_company_name VARCHAR(50),
            has_warranty VARCHAR(50),
            warranty VARCHAR(50)
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
