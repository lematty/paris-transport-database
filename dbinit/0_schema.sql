create table routes (
    route_id varchar(255),
    agency_id varchar(255), -- reference doesn't appear to be in the csvs
    route_short_name varchar(31),
    route_long_name varchar(255),
    route_desc varchar(255),
    route_type varchar(255),
    route_url varchar(255),
    route_color varchar(15),
    route_text_color varchar(15)
);

create table trips (
    trip_id varchar(255),
    route_id varchar(255),
    service_id varchar(255), -- sub component of trip_id key
    trip_headsign varchar(255),
    trip_short_name varchar(255),
    direction_id varchar(255),
    shape_id varchar(255)
);

create table stops (
    stop_id varchar(255),
    stop_code varchar(255),
    stop_name varchar(63),
    stop_desc varchar(255),
    stop_lat varchar(255),
    stop_lon varchar(255),
    location_type varchar(255),
    parent_station varchar(255)
);

create table transfers (
    transfer_id serial primary key not null, -- this doesn't exist in the csv
    from_stop_id varchar(255),
    to_stop_id varchar(255),
    transfer_type varchar(255),
    min_transfer_time varchar(255)
);

create table stop_times (
    stop_time_id serial primary key not null, -- this doesn't exist in the csv
    trip_id varchar(255),
    arrival_time varchar(63),
    departure_time varchar(63),
    stop_id varchar(255),
    stop_sequence varchar(255),
    stop_headsign varchar(255),  -- empty
    shape_dist_traveled varchar(255) -- empty
);

create table calendar (
    calendar_id serial primary key not null, -- this doesn't exist in the csv
    service_id varchar(255),
    monday varchar(255),
    tuesday varchar(255),
    wednesday varchar(255),
    thursday varchar(255),
    friday varchar(255),
    saturday varchar(255),
    sunday varchar(255),
    start_date varchar(255),
    end_date varchar(255)
);

create table calendar_dates (
    calendar_date_id serial primary key not null, -- this doesn't exist in the csv
    service_id varchar(255),
    date varchar(255),
    exception_type varchar(255)
);

create table agency (
    agency_id varchar(255),
    agency_name varchar(255),
    agency_url varchar(255),
    agency_timezone varchar(255),
    agency_lang varchar(255),
    agency_phone varchar(255)
);