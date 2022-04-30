#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE addresses (
      id SERIAL PRIMARY KEY,
      address VARCHAR NOT NULL
  );

	CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR NOT NULL,
	  email VARCHAR NOT NULL,
	  address_id INTEGER NOT NULL,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE
  );
EOSQL