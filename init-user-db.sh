#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
	email VARCHAR UNIQUE NOT NULL
  );

  CREATE TABLE addresses (
      id SERIAL PRIMARY KEY,
      user_id INTEGER NOT NULL,
      address VARCHAR NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users(id)
  );

EOSQL