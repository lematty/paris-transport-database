import csv
import re
import sys
import zipfile
from os import listdir
from os.path import isfile, join


def get_all_files(filepath: str) -> list:
    return [join(filepath, f) for f in listdir(filepath) if isfile(join(filepath, f))]


def add_quotes(val: str) -> str:
    x = val.replace("'", "''")
    return f"'{x}'"


def parse_csvfiles(csvfiles: list):
    for csvfile in csvfiles:
        base = re.sub(r'.*[/]', '', csvfile)

        statement = ""

        with open(csvfile, newline='\n') as f:
            reader = csv.DictReader(f)
            insert_prefix = f"INSERT INTO {base.split('.')[0]} ({','.join([k for k in reader.fieldnames])}) VALUES"

            statement += insert_prefix

            for row in reader:
                statement += f"\n({','.join([add_quotes(val[1]) for val in row.items()])}),"

            # replace last comma with a semi colon
            statement = statement[:-1] + ';'
            print(statement)

parse_csvfiles(get_all_files(sys.argv[1]))
