#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done
echo $SQL_HOST $SQL_PORT
echo "PostgreSQL started"

exec "$@"
