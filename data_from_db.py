import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('instance/user.db')
cursor = conn.cursor()

# Execute a SQL query to fetch data
cursor.execute("SELECT * FROM Users")

# Fetch data and convert to JSON
data = cursor.fetchall()

# Convert data to a list of dictionaries
column_names = [desc[0] for desc in cursor.description]
data_as_dicts = [dict(zip(column_names, row)) for row in data]

with open('data_db_without_ORM.json', 'w') as json_file:
        json.dump(data_as_dicts, json_file)

