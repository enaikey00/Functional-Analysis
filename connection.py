## Titolo: python x analisi funzionale
## Descrizione: 
## - connessione a un database SQL Server
## - estrazione tabelle, campi e tipi di dato
## TODO: scrittura su CSV o Word.
## Obiettivo: automatizzare la parte di "AS IS" del documento di Analisi Funzionale, in cui si descrivono le tabelle e i campi esistenti.
## UPGRADE: usare API ChatGPT per generare una descrizione del database (Introduzione dell'AS IS) ed eventualmente per suggerire analisi per il "TO BE"

import pyodbc
import json

server_name = "dev-sibi.database.windows.net"
database_name = "ITSKILLS-MATRIX-DEV"
username = "devsibi"
password = "xF6zC8egFkCj6Pt"

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server_name+';DATABASE='+database_name+';UID='+username+';PWD='+password)

cursor = conn.cursor()

#cursor.execute("SELECT * FROM dbo.COMPANIES")
table_names = [x[2] for x in cursor.tables(tableType='TABLE')]
# Dictionary to store column names for each table
columns_per_table = {}

# Loop through each table name
for table_name in table_names:
    # Execute the query to retrieve column names and data types for the current table
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE \
                    FROM INFORMATION_SCHEMA.COLUMNS \
                    WHERE TABLE_NAME = ?", table_name)
    
    # Fetch all rows and store column names and data types in a list of tuples
    columns_info = [(row.COLUMN_NAME, row.DATA_TYPE) for row in cursor.fetchall()]
    
    # Store column names and data types in the dictionary
    columns_per_table[table_name] = columns_info

# Printing column names and data types for each table
for table_name, columns_info in columns_per_table.items():
    print(f"Columns for table '{table_name}':")
    for column_name, data_type in columns_info:
        print(f"- {column_name}: {data_type}")

# Closing the cursor and connection
cursor.close()
conn.close()

# Save the dictionary into a JSON file
with open('columns_per_table.json', 'w') as f:
    json.dump(columns_per_table, f)