SHELL := /bin/bash

setup-everything:
	make clear-everything
	make create-schema
	make create-insert-statements
	make start-db

clear-everything:
	make shutdown-db
	make remove-dbinit
	make remove-data

create-schema:
	./createdb.bash schema

create-insert-statements:
	./createdb.bash

remove-dbinit:
	rm -rf dbinit

remove-data:
	rm -rf data

start-db:
	docker-compose -f docker-compose.yaml up

shutdown-db:
	docker-compose down --volumes
