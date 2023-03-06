CREATE SCHEMA IF NOT EXISTS sensors;

DROP TABLE IF EXISTS sensors.images CASCADE;
DROP TABLE IF EXISTS sensors.person CASCADE;
DROP TABLE IF EXISTS sensors.suspects CASCADE;

CREATE TABLE sensors.images(
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
    license_plates TEXT[]
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
	wanted_level INTEGER DEFAULT 0 CHECK (wanted_level >= 0 AND wanted_level <= 10),
	license_plates TEXT[],
	actions INTEGER[],
	social_net_words TEXT[],
	sensors TEXT[]
);

CREATE TABLE sensors.wanted (
    person_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	photo_src BYTEA NOT NULL,
	wanted_level INTEGER,
	wanted BOOL NOT NULL,
	actions INTEGER[],
	license_plates TEXT[],
	car_model TEXT[]
);

COMMIT;
