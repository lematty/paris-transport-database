#!/bin/bash

zippath="./source/buses/"

ziplist=($(ls ${zippath}*.zip))

mkdir -p dbinit

function work() {
    for f; do [[ -f $f ]] && process_zip "$f"; done
}

function process_zip() {
    name="${1##*/}"
    tmpdir="${name}_tmp"
    seen=$(ls dbinit | grep "$name")
    if [[ ${seen} != '' ]]; then
        continue
    fi

    mkdir -p ${tmpdir}
    unzip ${1} -d ${tmpdir}

    for t in ${tmpdir}/*.txt; do
        python ./csv2postgres.py ./${tmpdir} ${name}
    done
     rm -rf ${tmpdir}
}

if [[ "$1" == "schema" ]]; then
    python ./schema.py && mv 0_schema.sql dbinit
    exit 0
fi

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

mv *.sql dbinit