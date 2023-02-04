#!/bin/bash

zippath="./raw-data/"

ziplist=($(ls ${zippath}*.zip))

mkdir -p dbinit
mkdir -p raw-data

function work() {
    for f; do [[ -f $f ]] && process_zip "$f"; done
}

function process_zip() {
    directory="${1##*/}"
    tmpdir="${directory}_tmp"
    seen=$(ls dbinit | grep "$directory")
    if [[ ${seen} != '' ]]; then
        return
    fi

    mkdir -p ${tmpdir}
    unzip ${1} -d ${tmpdir}

    python3 ./csv2postgres.py ./${tmpdir} ${directory}

    echo "removing $tmpdir"
    rm -rf ${tmpdir}
}

if [[ "$1" == "schema" ]]; then
    curl -o "./${zippath}/transport-data.zip" https://data.iledefrance-mobilites.fr/api/v2/catalog/datasets/offre-horaires-tc-gtfs-idfm/files/a925e164271e4bca93433756d6a340d1
    python3 ./schema.py && mv 0_schema.sql dbinit
    exit 0
fi

if [[ ${#ziplist[*]} > 1 ]]; then
    echo "multiple gtfs files detected"
    # Divide the list into 5 sub-lists.
    i=0 n=0 a=() b=() c=() d=() e=()
    while ((i < ${#ziplist[*]})); do
        echo ${ziplist[i]}
        a[n]=${ziplist[i]}
        b[n]=${ziplist[i+1]}
        c[n]=${ziplist[i+2]}
        d[n]=${ziplist[i+3]}
        e[n]=${ziplist[i+4]}
        ((i+=5, n++))
    done

    # Process the sub-lists in parallel
    work "${a[@]}" &
    work "${b[@]}" &
    work "${c[@]}" &
    work "${d[@]}" &
    work "${e[@]}" &
    wait
else
    echo "one gtfs file detected"
    echo ${ziplist[0]}
    a=()
    a[0]=${ziplist[0]}
    work "${a[@]}" &
    wait
fi

echo "moving sql files to dbinit"
mv *.sql dbinit
