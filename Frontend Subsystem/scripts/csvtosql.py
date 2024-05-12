import csv
import sqlite3

# Connect to the SQLite database (create a new one if it doesn't exist)
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Open the CSV file
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Get the column names from the first row of the CSV file
    columns = next(csv_reader)

    # Create a table with the column names
    table_name = 'data_table'
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join([f"{column} TEXT" for column in columns])})'
    c.execute(create_table_query)

    # Insert data into the table
    insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["?"] * len(columns))})'
    c.executemany(insert_query, csv_reader)

# Commit the changes and close the connection
conn.commit()
conn.close()