import json
from typing import Dict, Union


def get_details_from_raw_json(json_data: Union[str, Dict]) -> Dict[str, Union[str, int, float]]:
    # Collect key-values of interest from json data.
    # Return a dictionary with keys (column names) and atomic values, which represent a row in table.
    # This looks for content under: object > props > pageProps > listingDetails

    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    listing_details = json_data['props']['pageProps']['listingDetails']
    vehicle = listing_details['vehicle']
    prices_public = listing_details['prices']['public']
    equipment = vehicle.get('equipment', {})
    equipment_comfort = equipment.get('comfortAndConvenience', [])
    equipment_entertainment = equipment.get('entertainmentAndMedia', [])
    equipment_safety = equipment.get('safetyAndSecurity', [])
    location = listing_details.get('location', {})
    seller = listing_details.get('seller', {})
    # print(json.dumps(listing_details, indent=2))

    row_as_dict = {
        'id': listing_details['id'],
        'vin': None,
        'price': prices_public['priceRaw'],
        'price_currency': 'EUR' if '\u20AC' in prices_public['price'] else '',
        'price_negotiable': prices_public.get('negotiable'),
        'price_tax_deductible': prices_public.get('taxDeductible'),
        'price_net': prices_public.get('netPriceRaw'),
        'vat_rate': prices_public.get('vatRate'),
        'make': vehicle['make'],
        'model': vehicle['model'],
        'model_version': vehicle.get('modelVersionInput'),
        'german_hsn_tsn': vehicle.get('hsnTsn'),
        'mileage_km': vehicle.get('mileageInKmRaw'),
        'production_year': vehicle.get('productionYear'),
        'registration_date': vehicle.get('firstRegistrationDateRaw'),
        'vehicle_type': vehicle['type'],
        'body_type': vehicle.get('bodyType'),
        'nr_seats': vehicle.get('numberOfSeats'),
        'nr_doors': vehicle.get('numberOfDoors'),
        'body_color': vehicle.get('bodyColor'),
        'paint_type': vehicle.get('paintType'),
        'body_color_original': vehicle.get('bodyColorOriginal'),
        'upholstery': vehicle.get('upholstery'),
        'upholstery_color': vehicle.get('upholsteryColor'),
        'power_hp': vehicle.get('rawPowerInHp'),
        'power_kw': vehicle.get('rawPowerInKw'),
        'transmission': vehicle.get('transmissionType'),
        'gears': vehicle.get('gears'),
        'cylinders': vehicle.get('cylinders'),
        'drive_train': vehicle.get('driveTrain'),
        'volume_ccm': vehicle.get('rawDisplacementInCCM'),
        'weight_kg': vehicle.get('weight'),
        'fuel_category': vehicle.get('fuelCategory', {}).get('formatted'),
        'primary_fuel': vehicle.get('primaryFuel', {}).get('formatted'),
        'fuel_cons_comb_l100km': vehicle.get('fuelConsumptionCombined', {}).get('raw'),
        'fuel_cons_city_l100km': vehicle.get('fuelConsumptionUrban', {}).get('raw'),
        'fuel_cons_highway_l100km': vehicle.get('fuelConsumptionExtraUrban', {}).get('raw'),
        'co2_emission_grperkm': vehicle.get('co2emissionInGramPerKm', {}).get('raw'),
        'has_particle_filter': vehicle.get('hasParticleFilter'),
        'electric_range_km': vehicle.get('electricRange', {}).get('raw'),
        'feats_cruise_control': int('Cruise control' in equipment_comfort),
        'feats_start_stop': int('Start-stop system' in equipment_comfort),
        'feats_electrical_side_mirrors': int('Electrical side mirrors' in equipment_comfort),
        'feats_electrical_adj_seats': int('Electrically adjustable seats' in equipment_comfort),
        'feats_headsup_disp': int('Heads-up display' in equipment_comfort),
        'feats_panorama_roof': int('Panorama roof' in equipment_comfort),
        'feats_auto_climate_control': int('Automatic climate control, 2 zones' in equipment_comfort
                                          or 'Automatic climate control, 4 zones' in equipment_comfort),
        'feats_seats_leather': int('Leather seats' in equipment_comfort),
        'feats_seats_massage': int('Massage seats' in equipment_comfort),
        'feats_seats_ventilation': int('Seat ventilation' in equipment_comfort),
        'feats_seats_heating': int('Seat heating' in equipment_comfort),
        'feats_light_sensor': int('Light sensor' in equipment_comfort),
        'feats_navigation': int('Navigation system' in equipment_comfort),
        'feats_pdc': int('Park Distance Control' in equipment_comfort),
        'feats_park_sens_front': int('Parking assist system sensors front' in equipment_comfort),
        'feats_park_sens_rear': int('Parking assist system sensors rear' in equipment_comfort),
        'feats_park_camera': int('Parking assist system camera' in equipment_comfort),
        'feats_power_windows': int('Power windows' in equipment_comfort),
        'feats_bluetooth': int('Bluetooth' in equipment_entertainment),
        'feats_onboard_computer': int('On-board computer' in equipment_entertainment),
        'feats_usb': int('USB' in equipment_entertainment),
        'feats_wifi': int('WLAN / WiFi hotspot' in equipment_entertainment),
        'feats_sound': int('Sound system' in equipment_entertainment),
        'feats_abs': int('ABS' in equipment_safety),
        'feats_adapt_cruise_control': int('Adaptive Cruise Control' in equipment_safety),
        'feats_alarm': int('Alarm system' in equipment_safety),
        'feats_central_lock_remote': int('Central door lock with remote control' in equipment_safety),
        'feats_dist_warn_sys': int('Distance warning system' in equipment_safety),
        'feats_emergency_brake_assist': int('Emergency brake assistant' in equipment_safety),
        'feats_lane_depart_warn_sys': int('Lane departure warning system' in equipment_safety),
        'feats_immobilizer': int('Immobilizer' in equipment_safety),
        'feats_tire_monitor': int('Tire pressure monitoring system' in equipment_safety),
        'feats_traction_control': int('Traction control' in equipment_safety),
        'feats_adapt_headlights': int('Adaptive headlights' in equipment_safety),
        'feats_xenon': int('Xenon headlights' in equipment_safety),
        'feats_laser': int('Laser headlights' in equipment_safety),
        'feats_led': int('LED Headlights' in equipment_safety),
        'envir_standard': vehicle.get('environmentEuDirective', {}).get('formatted'),
        'original_market': vehicle.get('originalMarket'),
        'offer_type': vehicle.get('offerType'),
        'is_used': int('Used' in vehicle.get('legalCategories', [])),
        'is_new': int('New' in vehicle.get('legalCategories', [])),
        'is_preregistered': int('Pre-registered' in vehicle.get('legalCategories', [])),
        'had_accident': vehicle.get('hadAccident'),
        'has_full_service_history': vehicle.get('hasFullServiceHistory'),
        'non_smoking': vehicle.get('nonSmoking'),
        'nr_prev_owners': vehicle.get('noOfPreviousOwners'),
        'is_rental': vehicle.get('isRental'),
        'country_code': location.get('countryCode'),
        'zip': location.get('zip'),
        'city': location.get('city'),
        'street': location.get('street'),
        'latitude': location.get('latitude'),
        'longitude': location.get('longitude'),
        'seller_is_dealer': seller.get('isDealer'),
        'seller_type': seller.get('type'),
        'seller_company_name': seller.get('companyName'),
        'has_warranty': seller.get('warrantyExists'),
        'warranty': seller.get('warranty'),
    }

    return row_as_dict