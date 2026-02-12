#!/usr/bin/bash

export $(grep '^DB_USER=' .env.dev)
export $(grep '^DB_HOST=' .env.dev)
export $(grep '^DB_PORT=' .env.dev)
export $(grep '^DB_NAME=' .env.dev)
dropdb -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME 

# rm */migrations/00*.py

