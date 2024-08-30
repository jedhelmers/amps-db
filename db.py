import csv
import os
import sqlite3

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect('amp_parts.db')
cursor = conn.cursor()

# Create tables with foreign keys
cursor.execute('''
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS amps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amp TEXT NOT NULL,
    brand_id INTEGER,
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS resistors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resistor INTEGER NOT NULL,
    wattage REAL,
    precision TEXT,
    amp_id INTEGER,
    FOREIGN KEY (amp_id) REFERENCES amps(id) ON DELETE SET NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS capacitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    capacitance REAL,
    electrolitic INTEGER,
    voltage_rating REAL,
    amp_id INTEGER,
    FOREIGN KEY (amp_id) REFERENCES amps(id) ON DELETE SET NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resistor INTEGER NOT NULL,
    wattage REAL,
    precision TEXT,
    taper TEXT,
    amp_id INTEGER,
    FOREIGN KEY (amp_id) REFERENCES amps(id) ON DELETE SET NULL
)
''')

# TUBES
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bias_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT UNIQUE NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tube_functionalities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tube_functionality TEXT UNIQUE NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tube_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT UNIQUE NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tubes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tube_type_id INTEGER,     -- Foreign key for tube type
        tube_functionality_id INTEGER,
        plate_voltage REAL,      -- Plate voltage in volts
        plate_current REAL,      -- Plate current in amps
        cathode_current REAL,    -- Cathode current in amps
        grid_current REAL,       -- Grid current in amps
        dissipation REAL,        -- Dissipation in watts
        bias REAL,               -- Bias voltage in volts
        bias_type_id INTEGER,    -- Foreign key for bias type
        amp_id INTEGER,
        datasheet_url TEXT,      -- URL or file path to the datasheet
        FOREIGN KEY (tube_type_id) REFERENCES tube_types(id) ON DELETE SET NULL,
        FOREIGN KEY (bias_type_id) REFERENCES bias_types(id) ON DELETE SET NULL,
        FOREIGN KEY (tube_functionality_id) REFERENCES tube_functionalities(id) ON DELETE SET NULL,
        FOREIGN KEY (amp_id) REFERENCES amps(id) ON DELETE SET NULL
    );
""")

# Transformers
cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS transformer_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT
    );
"""
)

cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS winding_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT
    );
"""
)

cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS core_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT
    );
"""
)

cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS transformers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number TEXT,
        transformer_type_id INTEGER,
        core_type_id INTEGER,
        wattage REAL,
        amp_id INTEGER,
        FOREIGN KEY (core_type_id) REFERENCES core_types(id) ON DELETE SET NULL,
        FOREIGN KEY (transformer_type_id) REFERENCES transformer_types(id) ON DELETE SET NULL,
        FOREIGN KEY (amp_id) REFERENCES amps(id) ON DELETE SET NULL
    );
"""
)

cursor.execute(
"""
    CREATE TABLE IF NOT EXISTS transformer_windings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transformer_id INTEGER,
        winding_type_id TEXT,
        volts TEXT,
        amps REAL,
        impedance REAL,
        FOREIGN KEY (winding_type_id) REFERENCES winding_type(id) ON DELETE SET NULL,
        FOREIGN KEY (transformer_id) REFERENCES transformers(id) ON DELETE SET NULL
    );
"""
)


# Commit changes and close the connection
conn.commit()
conn.close()


def import_csv_to_db(file_path, table_name):
    conn = sqlite3.connect('amp_parts.db')
    cursor = conn.cursor()
    
    # Read CSV file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        # Get the header row as the column names
        columns = next(reader)
        
        # Prepare placeholders for SQL queries
        placeholders = ', '.join(['?' for _ in columns])
        query = f'INSERT OR IGNORE INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
        
        # Read the remaining rows
        rows = [tuple(row) for row in reader]
    
    # Execute the insert query with error handling
    try:
        cursor.executemany(query, rows)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    # Close the connection
    conn.close()

def import_data():
    base_url = "./parts/"

    # Import data
    import_csv_to_db(os.path.join(base_url, 'bias_types.csv'), 'bias_types')
    import_csv_to_db(os.path.join(base_url, 'tube_functionalities.csv'), 'tube_functionalities')
    import_csv_to_db(os.path.join(base_url, 'amps.csv'), 'amps')
    import_csv_to_db(os.path.join(base_url, 'brands.csv'), 'brands')
    import_csv_to_db(os.path.join(base_url, 'tube_types.csv'), 'tube_types')
    import_csv_to_db(os.path.join(base_url, 'transformer_types.csv'), 'transformer_types')
    import_csv_to_db(os.path.join(base_url, 'winding_types.csv'), 'winding_types')
    import_csv_to_db(os.path.join(base_url, 'core_types.csv'), 'core_types')

    amps = ['vibro-champ']

    for amp in amps:
        import_csv_to_db(os.path.join(base_url, amp, 'tubes.csv'), 'tubes')
        import_csv_to_db(os.path.join(base_url, amp, 'resistors.csv'), 'resistors')
        import_csv_to_db(os.path.join(base_url, amp, 'capacitors.csv'), 'capacitors')
        import_csv_to_db(os.path.join(base_url, amp, 'pots.csv'), 'pots')
        import_csv_to_db(os.path.join(base_url, amp, 'transformer_windings.csv'), 'transformer_windings')
        import_csv_to_db(os.path.join(base_url, amp, 'transformers.csv'), 'transformers')
