## Description
Database creation for Paris transportation systems.

This repository will do the following:
1. Download the zip file containing the trasport data.
2. Unzip and create database schema.
3. Build insert queries from downloaded files.
4. Create a postgres database with tables.
5. Insert data into tables.

# Prerequisites
You will need [Python 3.7](https://www.python.org/downloads/) and [Docker](https://www.docker.com/) installed.

You can check if installed with:
```bash
# Python 3.7
python3.7 --version

# Docker
docker --version
```

# Download data
Use the following command to download the zip file containing the data. This data changes every 3 weeks.

# Initializing the database
```bash
# clear old insert statements before starting. Note that this data changes every 3 weeks.
rm -rf dbinit

# clear database data
docker-compose down --volumes

# create database schema
./createdb.bash schema

# create insert statements (this may take a while)
./createdb.bash

# launch db
docker-compose -f docker-compose.yaml up
```
