import pandas as pd
import sqlite3

# Function to create the SQLite database and tables
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Manufacturer (
        manufacturer_id INTEGER PRIMARY KEY,
        name TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Animal (
        animal_id INTEGER PRIMARY KEY,
        name TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        manufacturer_id INTEGER,
        weight DECIMAL,
        flavor TEXT,
        target_health_condition TEXT,
        material TEXT,
        durability TEXT,
        color TEXT,
        size TEXT,
        care_instructions TEXT,
        FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer(manufacturer_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product_Animal (
        product_id INTEGER,
        animal_id INTEGER,
        PRIMARY KEY (product_id, animal_id),
        FOREIGN KEY (product_id) REFERENCES Product(product_id),
        FOREIGN KEY (animal_id) REFERENCES Animal(animal_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transaction (
        transaction_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        date DATE,
        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Transaction_Product (
        transaction_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        PRIMARY KEY (transaction_id, product_id),
        FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id),
        FOREIGN KEY (product_id) REFERENCES Product(product_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Location (
        location_id INTEGER PRIMARY KEY,
        name TEXT,
        zip_code TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shipment (
        shipment_id INTEGER PRIMARY KEY,
        origin_id INTEGER,
        destination_id INTEGER,
        FOREIGN KEY (origin_id) REFERENCES Location(location_id),
        FOREIGN KEY (destination_id) REFERENCES Location(location_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shipment_Product (
        shipment_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        PRIMARY KEY (shipment_id, product_id),
        FOREIGN KEY (shipment_id) REFERENCES Shipment(shipment_id),
        FOREIGN KEY (product_id) REFERENCES Product(product_id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to read and insert data from Spreadsheet 0
def insert_spreadsheet_0(db_file, spreadsheet_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Read spreadsheet 0
    df = pd.read_excel(spreadsheet_file, sheet_name='Spreadsheet_0')

    # Insert data into Product table
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT INTO Product (name, type, manufacturer_id, weight, flavor, target_health_condition,
                             material, durability, color, size, care_instructions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Name'], row['Type'], row['Manufacturer ID'], row['Weight'], row['Flavor'],
              row['Target Health Condition'], row['Material'], row['Durability'],
              row['Color'], row['Size'], row['Care Instructions']))

    conn.commit()
    conn.close()

# Function to read and insert data from Spreadsheet 1 and 2
def insert_spreadsheet_1_2(db_file, spreadsheet1_file, spreadsheet2_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Read spreadsheet 1 (Shipments)
    df_shipments = pd.read_excel(spreadsheet1_file, sheet_name='Spreadsheet_1')

    # Read spreadsheet 2 (Locations)
    df_locations = pd.read_excel(spreadsheet2_file, sheet_name='Spreadsheet_2')

    # Insert data into Shipment and Shipment_Product tables
    for index, row in df_shipments.iterrows():
        origin_id = df_locations[df_locations['Shipping ID'] == row['Shipping ID']]['Origin ID'].values[0]
        destination_id = df_locations[df_locations['Shipping ID'] == row['Shipping ID']]['Destination ID'].values[0]

        cursor.execute('''
        INSERT INTO Shipment (shipment_id, origin_id, destination_id)
        VALUES (?, ?, ?)
        ''', (row['Shipping ID'], origin_id, destination_id))

        products = row['Products'].split(',')
        quantities = row['Quantities'].split(',')

        for i in range(len(products)):
            product_id = int(products[i].strip())
            quantity = int(quantities[i].strip())

            cursor.execute('''
            INSERT INTO Shipment_Product (shipment_id, product_id, quantity)
            VALUES (?, ?, ?)
            ''', (row['Shipping ID'], product_id, quantity))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Replace with the path to your SQLite database file
    db_file = 'C:\Users\mishr\OneDrive\Harshit\forage-walmart-task-4\shipment_database.db'

    # Create database schema
    create_database(db_file)

    # Insert data from Spreadsheet 0
    spreadsheet0_file = 'C:\Users\mishr\OneDrive\Harshit\forage-walmart-task-4\data\shipping_data_0.csv'
    insert_spreadsheet_0(db_file, spreadsheet0_file)

    # Insert data from Spreadsheet 1 and 2
    spreadsheet1_file = 'C:\Users\mishr\OneDrive\Harshit\forage-walmart-task-4\data\shipping_data_1.csv'
    spreadsheet2_file = 'C:\Users\mishr\OneDrive\Harshit\forage-walmart-task-4\data\shipping_data_2.csv'
    insert_spreadsheet_1_2(db_file, spreadsheet1_file, spreadsheet2_file)

    print("Data insertion completed.")