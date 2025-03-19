import csv
import os
from dotenv import load_dotenv
import psycopg2

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

def fetch_and_print(cur, query):
    cur.execute(query)
    records = cur.fetchall()
    
    # Print column names and records
    colnames = [desc[0] for desc in cur.description]
    print(colnames)
    cleaned_records = []
    for record in records:
        cleaned_record = [str(field).replace("\n", " ").replace("\r", " ") if isinstance(field, str) else field for field in record]
        cleaned_records.append(cleaned_record)
        print(record)

    return cleaned_records, colnames


def write_to_csv(records, colnames, output_file="../VBE-library/data_output/db_output.csv"):
    # Ensure the directory exists; if not, create it
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Open the file and write to it
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        
        # Write header (column names) and rows (records)
        writer.writerow(colnames)
        writer.writerows(records)

    print(f"Records written to {output_file}")


def view_all_tab_cols(cur, csv_flag):
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
    
    cleaned_records, colnames = fetch_and_print(cur, query)

    if csv_flag == "Y":
        write_to_csv(cleaned_records, colnames, output_file="../VBE-library/data_output/db_tab_cols.csv")


def preset_query(cur, table_name, query_name, csv_flag):
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
    
    # Fetch and print records
    cleaned_records, colnames = fetch_and_print(cur, query)

    # Write records to a CSV file
    if csv_flag == "Y":
        write_to_csv(cleaned_records, colnames, output_file="../VBE-library/data_output/db_output.csv")

# Main function
if __name__ == "__main__":
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("SET search_path TO public;")

        # Change below to Y to write to CSV
        csv_flag = "Y"

        # Uncomment below to view all tables and columns in the database
        view_all_tab_cols(cur, csv_flag)

        # Uncomment below to use a preset query
        query_name = "selectall" # selectall, countrecords, distinct, custom
        table_name = "vbe_dao" # dao, proposals, vbe_dao, votes, forums
        preset_query(cur, table_name, query_name, csv_flag)

        # Uncomment below to create your own custom query
        # custom_query = """
        # SELECT * FROM proposals 
        # WHERE dao_id = 'opcollective.eth';
        # """
        # cleaned_records, colnames = fetch_and_print(cur, custom_query)
        # if csv_flag == "Y":
        #     write_to_csv(cleaned_records, colnames, output_file="data/db_custom_query.csv")

    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")