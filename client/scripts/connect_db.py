from os import environ

PG_CONNECT = {
    "dbname": environ.get("PG_DATABASE"),
    "user": environ.get("PG_USER"),
    "password": environ.get("PG_PASSWORD"),
    "host": environ.get("PG_HOST"),
    "port": environ.get("PG_PORT"),
}