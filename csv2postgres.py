import csv
import re
import sys
import zipfile
from os import listdir
from os.path import isfile, join

from schema import init_db_schema

insert_stmts = {}


def write(filename: str, stmt: str): 
    with open(filename, "w") as f:
        f.write(stmt)


def get_all_files(filepath: str) -> list:
    return [join(filepath, f) for f in listdir(filepath) if isfile(join(filepath, f))]


def insert_repr(table: object, val: dict) -> str:
    return table.get_column(val[0]).insert_repr(val[1])


def parse_csvfiles(db: object, csvfiles: list, filename: str):
    for csvfile in csvfiles:
        base = re.sub(r'.*[/]', '', csvfile)
        table_name = base.split('.')[0]
        table = db.get_table(table_name)
        if table is None:
            continue

        statement = ""

        with open(csvfile, newline='\n') as f:
            reader = csv.DictReader(f)
            insert_prefix = f"INSERT INTO {table_name} ({','.join([k for k in reader.fieldnames])}) VALUES"

            statement += insert_prefix

            for row in reader:
                statement += f"\n({','.join([insert_repr(table, val) for val in row.items()])}),"

            # replace last comma with a semi colon
            statement = statement[:-1] + ';'

            insert_stmts[table_name] = statement

    for (i, t) in enumerate(db.insert_order):
        write(f"{i+1}_{t.name}_{filename}.sql", insert_stmts[t.name])

db = init_db_schema()
parse_csvfiles(db, get_all_files(sys.argv[1]), sys.argv[2])
