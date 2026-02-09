import pandas as pd
from sqlalchemy import create_engine
import time

# ---------------- CONFIGURATION ----------------
# Database connection details (matching your docker-compose)
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5433' # IMPORTANT: Use the host port mapped in docker-compose
DB_NAME = 'ny_taxi'

# Data URLs
URL_TRIPS = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
URL_ZONES = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

# Table Names
TABLE_TRIPS = "green_tripdata"
TABLE_ZONES = "zones"

def main():
    # 1. Create SQL Engine
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
    print("Connecting to database...")

    # 2. Ingest Taxi Zones (CSV)
    print(f"Downloading and reading {URL_ZONES}...")
    df_zones = pd.read_csv(URL_ZONES)
    
    print(f"Writing {len(df_zones)} rows to table '{TABLE_ZONES}'...")
    df_zones.to_sql(name=TABLE_ZONES, con=engine, if_exists='replace', index=False)
    print("Zones ingested successfully!")

    # 3. Ingest Green Taxi Data (Parquet)
    print(f"Downloading and reading {URL_TRIPS}...")
    # Parquet is efficient, we can usually load it all at once for monthly files
    df_trips = pd.read_parquet(URL_TRIPS)

    print(f"Writing {len(df_trips)} rows to table '{TABLE_TRIPS}'...")
    
    # We use chunksize to avoid sending too much data at once
    # method='multi' helps speed up inserts slightly
    start_time = time.time()
    df_trips.to_sql(name=TABLE_TRIPS, con=engine, if_exists='replace', index=False, chunksize=10000)
    end_time = time.time()

    print(f"Trips ingested successfully in {end_time - start_time:.2f} seconds!")

if __name__ == '__main__':
    main()