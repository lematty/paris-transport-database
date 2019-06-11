#!/bin/bash

zippath="../src/assets/geojson/source/Buses/"

mkdir ziptmp

for z in ${zippath}/*.zip; do
    sqlout="${z##*/}.sql"
    rm -f ziptmp/*
    unzip ${z} -d ziptmp

    for t in ziptmp/*.txt; do
        echo ${t}
        python ./csv2postgres.py ./ziptmp > dbinit/${sqlout}
    done
done

rm -rf ziptmp