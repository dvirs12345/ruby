CREATE SCHEMA IF NOT EXISTS sensors;

DROP TABLE IF EXISTS sensors.images CASCADE;

CREATE TABLE sensors.images(
	camera_id TEXT PRIMARY KEY,
	longitude INTEGER NOT NULL,
	latitude INTEGER NOT NULL,
	image_src BYTEA,
	sensors_timestamp TIMESTAMP
);

COMMIT;
