DROP TABLE IF EXISTS yellow_tripdata;
DROP TABLE IF EXISTS green_tripdata;

CREATE TABLE yellow_tripdata (
    VendorID text,
    tpep_pickup_datetime timestamp without time zone,
    tpep_dropoff_datetime timestamp without time zone,
    passenger_count integer,
    trip_distance double precision,
    RatecodeID text,
    store_and_fwd_flag text,
    PULocationID text,
    DOLocationID text,
    payment_type text,
    fare_amount double precision,
    extra double precision,
    mta_tax double precision,
    tip_amount double precision,
    tolls_amount double precision,
    improvement_surcharge double precision,
    total_amount double precision,
    congestion_surcharge double precision
);

CREATE TABLE green_tripdata (
    VendorID text,
    lpep_pickup_datetime timestamp without time zone,
    lpep_dropoff_datetime timestamp without time zone,
    store_and_fwd_flag text,
    RatecodeID text,
    PULocationID text,
    DOLocationID text,
    passenger_count integer,
    trip_distance double precision,
    fare_amount double precision,
    extra double precision,
    mta_tax double precision,
    tip_amount double precision,
    tolls_amount double precision,
    ehail_fee double precision,
    improvement_surcharge double precision,
    total_amount double precision,
    payment_type text,
    trip_type text,
    congestion_surcharge double precision
);
