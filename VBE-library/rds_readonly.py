import csv
import os
from dotenv import load_dotenv
import psycopg2
import database as db

# Load environment variables from .env file
load_dotenv()

# Database connection
db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def print_records(cur, table_name, query_name, csv_flag):
    if query_name == "selectall":
        query = "SELECT * FROM " + table_name + ";"
    elif query_name == "countrecords":
        query = "SELECT COUNT(*) FROM " + table_name + ";"
    elif query_name == "distinct":
        query = "SELECT DISTINCT id FROM " + table_name + ";"
    elif query_name == "custom":
        # Create your own query below
        query = ""
    else:
        print("Invalid query name.")
        return
    cur.execute(query)
    records = cur.fetchall()
    
    # Print column names and records
    colnames = [desc[0] for desc in cur.description]
    print(colnames)
    for record in records:
        print(record)

    # Write records to a CSV file
    if csv_flag == "Y":
        output_file = "data/db_output.csv"
        # Ensure the directory exists; if not, create it
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Open the file and write to it
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write header (column names)
            writer.writerow(colnames)
            
            # Write all rows
            writer.writerows(records)

    print(f"Records written to {output_file}")

def view_all_tab_cols(cur):
    query="""
    SELECT 
    c.table_name, 
    c.column_name, 
    c.data_type, 
    c.is_nullable,
    tc.constraint_type
    FROM 
        information_schema.columns c
    LEFT JOIN 
        information_schema.constraint_column_usage ccu 
    ON 
        c.table_name = ccu.table_name AND c.column_name = ccu.column_name
    LEFT JOIN 
        information_schema.table_constraints tc 
    ON 
        ccu.constraint_name = tc.constraint_name
    WHERE 
        c.table_schema = 'public'
    ORDER BY 
        c.table_name, c.ordinal_position;
    """
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    print(colnames)
    # Print each row
    for row in rows:
        print(row)

# Main function
if __name__ == "__main__":
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SET search_path TO public;")

        # View all tables and columns in the database
        # view_all_tab_cols(cur)
        
        # EDIT THE BELOW VARIABLES AS NEEDED
        query_name = "selectall" # selectall, countrecords, distinct, custom
        table_name = "dao" # dao, proposals, vbe_dao, votes, forums
        csv_flag = "Y"  # Y or N to write to CSV
        
        # Query to select rows from database to read
        print_records(cur, table_name, query_name, csv_flag)  # Print all records in the table
        
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")