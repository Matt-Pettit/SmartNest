import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Function to show all results
def show_all_results():
    c.execute("SELECT * FROM data_table")
    rows = c.fetchall()
    for row in rows:
        print(row)
    return rows

# Function to add a new result
def add_new_result():
    new_row = input("Enter a comma-separated list of values: ").split(",")
    values = [val.strip() for val in new_row]
    c.execute(f"INSERT INTO data_table VALUES ({', '.join(['?'] * len(values))})", values)
    conn.commit()
    print("New result added successfully.")

# Function to show results from a certain date range
def show_results_date_range():
    start_date = input("Enter start date (YYYY/MM/DD): ")
    end_date = input("Enter end date (YYYY/MM/DD): ")
    c.execute("SELECT * FROM data_table WHERE Timestamp BETWEEN ? AND ?", (f"{start_date} 00:00", f"{end_date} 23:59"))
    rows = c.fetchall()
    for row in rows:
        print(row)
    return rows

# Function to delete a record
def delete_record():
    record_id = input("Enter the ID of the record to delete: ")
    c.execute("DELETE FROM data_table WHERE id = ?", (record_id,))
    conn.commit()
    print(f"Record with ID {record_id} deleted successfully.")

# Example usage
print("1. Show all results")
print("2. Add a new result")
print("3. Show results from a date range")
print("4. Delete a record")
print("5. Exit")

while True:
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        results = show_all_results()
    elif choice == "2":
        add_new_result()
    elif choice == "3":
        results = show_results_date_range()
    elif choice == "4":
        delete_record()
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()