CREATE SCHEMA IF NOT EXISTS sensors;

DROP TABLE IF EXISTS sensors.images CASCADE;
DROP TABLE IF EXISTS sensors.person CASCADE;
DROP TABLE IF EXISTS sensors.suspects CASCADE;
DROP TABLE IF EXISTS sensors.wanted CASCADE;

CREATE TABLE sensors.images(
	image_id SERIAL,
	camera_id TEXT,
	longitude FLOAT NOT NULL,
	latitude FLOAT NOT NULL,
	image_src BYTEA,
	sensors_timestamp TIMESTAMP
);

CREATE TABLE sensors.person (
    person_id SERIAL PRIMARY KEY,
	photo_url TEXT NOT NULL,
    first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	address TEXT,
	date_of_birth DATE NOT NULL,
	city TEXT NOT NULL,
	wanted BOOL NOT NULL,
	work_visa BOOL NOT NULL,
	actions INTEGER[],
	social_net_words TEXT[],
    license_plates TEXT[],
);

CREATE TABLE sensors.suspects (
    suspect_id SERIAL PRIMARY KEY,
	photo_url TEXT NOT NULL,
    first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	address TEXT,
	date_of_birth DATE NOT NULL,
	city TEXT NOT NULL,
	work_visa BOOL NOT NULL,
	wanted_level INTEGER,
	license_plates TEXT[],
	actions INTEGER[],
	social_net_words TEXT[],
	sensors TEXT[]
);

CREATE TABLE sensors.wanted (
	person_id TEXT PRIMARY KEY,
    photo_url TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    address TEXT,
    city TEXT NOT NULL,
    wanted BOOL NOT NULL,
    wanted_level INTEGER,
    actions INTEGER[],
    license_plates TEXT[],
    car_model TEXT[],
    work_visa BOOL
);

COMMIT;
