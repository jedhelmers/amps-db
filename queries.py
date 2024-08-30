import json
import sqlite3
from typing import Dict, List

import utilities


def get_db_connection():
    return sqlite3.connect('amp_parts.db')

def get_all_resistors_by_brand(brand_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT r.id, r.resistor, r.wattage, r.precision, r.amp_id
    FROM resistors r
    JOIN amps a ON r.amp_id = a.id
    JOIN brands b ON a.brand_id = b.id
    WHERE b.brand = ?
    '''
    
    cursor.execute(query, (brand_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **resistor,
            resistor: utilities.convert_resistor_value(resistor['resistor'])
        }
        for resistor in results
    ]

def get_all_capacitors_by_brand(brand_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT c.id, c.capacitance, c.electrolitic, c.voltage_rating, c.amp_id
    FROM capacitors c
    JOIN amps a ON c.amp_id = a.id
    JOIN brands b ON a.brand_id = b.id
    WHERE b.brand = ?
    '''
    
    cursor.execute(query, (brand_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **cap,
            'capacitance': utilities.convert_capacitor_value(cap['capacitance'])
        }
        for cap in results
    ]

def get_all_pots_by_brand(brand_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT p.id, p.resistor, p.wattage, p.precision, p.taper, p.amp_id
    FROM pots p
    JOIN amps a ON p.amp_id = a.id
    JOIN brands b ON a.brand_id = b.id
    WHERE b.brand = ?
    '''
    
    cursor.execute(query, (brand_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **resistor,
            resistor: utilities.convert_resistor_value(resistor['resistor'])
        }
        for resistor in results
    ]

def get_all_parts_by_brand(brand_name: str) -> List[Dict]:
    resistors = get_all_resistors_by_brand(brand_name)
    capacitors = get_all_capacitors_by_brand(brand_name)
    pots = get_all_pots_by_brand(brand_name)
    
    # Combine all parts into a single list
    all_parts = {
        'resistors': resistors,
        'capacitors': capacitors,
        'pots': pots
    }
    
    return all_parts

def get_all_brands() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT brand FROM brands'
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    brands = [row[0] for row in rows]
    
    conn.close()
    return brands

def get_all_resistors_by_amp_grouped(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT r.resistor, r.wattage, r.precision, COUNT(r.id) AS resistor_count
    FROM resistors r
    JOIN amps a ON r.amp_id = a.id
    WHERE a.amp = ?
    GROUP BY r.resistor, r.wattage, r.precision
    ORDER BY resistor_count DESC
    '''
    
    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **resistor,  # Merge the resistor dictionary
            'resistor': utilities.convert_resistor_value(resistor['resistor'])  # Convert and replace resistor value
        }
        for resistor in results
    ]

def get_all_resistors_by_amp(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT r.id, r.resistor, r.wattage, r.precision, r.amp_id
    FROM resistors r
    JOIN amps a ON r.amp_id = a.id
    WHERE a.amp = ?
    ORDER BY r.resistor DESC
    '''
    
    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **resistor,  # Merge the resistor dictionary
            'resistor': utilities.convert_resistor_value(resistor['resistor'])  # Convert and replace resistor value
        }
        for resistor in results
    ]

def get_all_capacitors_by_amp_grouped(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT c.id, c.capacitance, c.electrolitic, c.voltage_rating, COUNT(c.id) AS cap_count
    FROM capacitors c
    JOIN amps a ON c.amp_id = a.id
    WHERE a.amp = ?
    GROUP BY c.capacitance, c.electrolitic, c.voltage_rating
    ORDER BY cap_count DESC
    '''
    
    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()

    # return results
    return [
        {
            **cap,
            'capacitance': utilities.convert_capacitor_value(cap['capacitance'])
        }
        for cap in results
    ]


def get_all_capacitors_by_amp(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT c.id, c.capacitance, c.electrolitic, c.voltage_rating, c.amp_id
    FROM capacitors c
    JOIN amps a ON c.amp_id = a.id
    WHERE a.amp = ?
    ORDER BY c.capacitance ASC
    '''
    
    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **cap,
            'capacitance': utilities.convert_capacitor_value(cap['capacitance'])
        }
        for cap in results
    ]

def get_all_pots_by_amp(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT p.id, p.resistor, p.wattage, p.precision, p.taper, p.amp_id
    FROM pots p
    JOIN amps a ON p.amp_id = a.id
    WHERE a.amp = ?
    ORDER BY p.resistor ASC
    '''
    
    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return [
        {
            **pot,
            'resistor': utilities.convert_resistor_value(pot['resistor'])
        }
        for pot in results
    ]

def get_all_tubes_by_amp(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the amp_id for the given amp_name
    cursor.execute('''
    SELECT id
    FROM amps
    WHERE amp = ?
    ''', (amp_name,))
    amp_id_row = cursor.fetchone()
    
    if not amp_id_row:
        conn.close()
        return []  # No amp found with the given name
    
    amp_id = amp_id_row[0]
    
    # Get all tubes associated with the amp_id
    cursor.execute('''
    SELECT tubes.id, tubes.name, tube_types.type, tube_functionalities.tube_functionality,
           tubes.plate_voltage, tubes.plate_current, tubes.cathode_current, tubes.grid_current,
           tubes.dissipation, tubes.bias, bias_types.type AS bias_type, tubes.datasheet_url
    FROM tubes
    LEFT JOIN tube_functionalities ON tubes.id = tube_functionalities.id
    LEFT JOIN bias_types ON tubes.bias_type_id = bias_types.id
    LEFT JOIN tube_types ON tubes.tube_type_id = tube_types.id
    WHERE tubes.amp_id = ?
    ''', (amp_id,))
    
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    tubes = [dict(zip(columns, row)) for row in rows]
    
    conn.close()
    return tubes

def get_all_transformers_by_amp(amp_name: str) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            t.id AS transformer_id,
            a.amp,
            t.part_number,
            t.wattage,
            tt.type AS transformer_type,
            ct.type AS core_type,
            GROUP_CONCAT(
                json_object(
                    'id', tw.id,
                    'winding_type', wt.type,
                    'volts', tw.volts,
                    'amps', tw.amps
                )
            ) AS windings
        FROM
            transformers t
        LEFT JOIN
            transformer_types tt ON t.transformer_type_id = tt.id
        LEFT JOIN
            core_types ct ON t.core_type_id = ct.id
        LEFT JOIN
            transformer_windings tw ON t.id = tw.transformer_id
        LEFT JOIN
            winding_types wt ON tw.winding_type_id = wt.id
        JOIN amps a ON t.amp_id = a.id
            WHERE a.amp = ?
        GROUP BY
            t.id;

    """

    cursor.execute(query, (amp_name,))
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in rows]
    
    conn.close()

    return [
        {
            **transformer,
            'windings': [
                {
                    **winding,
                    'amps': utilities.convert_current_value(winding['amps'])
                }
                for winding in json.loads(f"[{transformer['windings']}]")
            ]
        }
        for transformer in results
    ]

def get_all_parts_by_amp(amp_name: str) -> Dict[str, List[Dict]]:
    resistors = get_all_resistors_by_amp(amp_name)
    capacitors = get_all_capacitors_by_amp(amp_name)
    pots = get_all_pots_by_amp(amp_name)
    tubes = get_all_tubes_by_amp(amp_name)
    
    all_parts = {
        'resistors': resistors,
        'capacitors': capacitors,
        'pots': pots,
        'tubes': tubes,
    }
    
    return all_parts

def get_all_amps() -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = '''
    SELECT b.brand, a.id AS amp_id, a.amp
    FROM amps a
    JOIN brands b ON a.brand_id = b.id
    ORDER BY b.brand, a.amp
    '''
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Create a dictionary to group amps by brand
    amps_by_brand = {}
    
    for row in rows:
        brand = row[0]
        amp_id = row[1]
        amp_name = row[2]
        
        if brand not in amps_by_brand:
            amps_by_brand[brand] = []
        
        amps_by_brand[brand].append({
            'id': amp_id,
            'amp': amp_name
        })
    
    conn.close()
    return amps_by_brand
