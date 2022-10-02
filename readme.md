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
```bash
# navigate to raw-data folder to download the file
cd raw-data

# download zip file transport-data.zip
curl -o transport-data.zip https://data.iledefrance-mobilites.fr/api/v2/catalog/datasets/offre-horaires-tc-gtfs-idfm/files/a925e164271e4bca93433756d6a340d1
```

# Initializing the database
```bash
# clear old data before starting
rm -rf dbinit

# create database schema
./createdb.bash schema

# build database and insert data (this may take a while)
./createdb.bash
```