SHELL := /bin/bash

create-schema:
	./createdb.bash schema

create-insert-statements:
	./createdb.bash

create-dbinit:
	make remove-dbinit
	make create-schema
	make create-insert-statements

remove-dbinit:
	rm -rf dbinit

start-db:
	docker-compose -f docker-compose.yaml up

clear-db:
	docker-compose down --volumes

