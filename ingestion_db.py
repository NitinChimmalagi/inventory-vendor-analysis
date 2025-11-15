import pandas as pd
import os
from sqlalchemy import create_engine
import sqlite3
import logging
import time

# Ensure log folder exists
if not os.path.exists("log"):
    os.makedirs("log")

# Setup logging
logging.basicConfig(
    filename="log/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create SQLite engine
engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    """Ingest a DataFrame chunk into the database table."""
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

def load_raw_data():
    """Load CSVs from 'Data' folder and ingest into SQLite database."""
    start = time.time()
    for file in os.listdir('Data'):
        if file.endswith('.csv'):
            file_path = os.path.join('Data', file)
            table_name = os.path.splitext(file)[0]  # safer than file[:-4]
            logging.info(f"Starting ingestion for {file} into table '{table_name}'")

            try:
                chunk_count = 0
                for chunk in pd.read_csv(file_path, chunksize=10000):
                    chunk_count += 1
                    logging.info(f"Ingesting chunk {chunk_count} with {len(chunk)} rows")
                    ingest_db(chunk, table_name, engine)
            except Exception as e:
                logging.error(f"Error processing {file}: {e}")
            else:
                elapsed = (time.time() - start) / 60
                logging.info(f"Finished ingestion for {file} in {elapsed:.2f} minutes")
    logging.info("✅ All ingestion complete.")

def verify_ingestion():
    """Verify row counts for all tables in the database."""
    conn = sqlite3.connect("inventory.db")
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

    if tables.empty:
        print("⚠️ No tables found in the database.")
    else:
        print("📊 Row counts per table:")
        for table in tables['name']:
            count = pd.read_sql(f"SELECT COUNT(*) AS row_count FROM {table};", conn)
            print(f" - {table}: {count['row_count'][0]} rows")
    conn.close()

if __name__ == '__main__':
    load_raw_data()
    verify_ingestion()