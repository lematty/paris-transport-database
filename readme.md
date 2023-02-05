## Description
Database creation for Paris transportation systems.

This repository will do the following:
1. Download the zip file containing the trasport data.
2. Unzip and create database schema.
3. Build insert queries from downloaded files.
4. Create a postgres database with tables.
5. Insert data into tables.

# Prerequisites
You will need:
- [Python 3.7](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Postgres](https://www.postgresql.org/)

You can check if installed with:
```bash
# Python 3.7
python3.7 --version

# Docker
docker --version

# Postgres
psql --version
```

# Initializing the database
```bash
# create database schema & insert statements (this may take a while)
make create-dbinit

# remove database schema & insert statements. Note that this data changes every 3 weeks.
make remove-dbinit

# launch database
make start-db

# clear database data (db needs to be running if clearing old data)
make clear-db
```
