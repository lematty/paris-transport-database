#!/bin/bash

zippath="./source/buses/"
mkdir -p dbinit
mkdir -p ziptmp

if [[ "$1" == "schema" ]]; then
    python ./schema.py && mv 0_schema.sql dbinit
    exit 0
fi

for z in ${zippath}/*.zip; do
    name="${z##*/}"
    seen=$(ls dbinit | grep "$name")
    if [[ ${seen} != '' ]]; then
        continue
    fi

    rm -f ziptmp/*
    unzip ${z} -d ziptmp

    for t in ziptmp/*.txt; do
        echo ${t}
        python ./csv2postgres.py ./ziptmp ${name} && mv *.sql dbinit
    done
done

rm -rf ziptmp