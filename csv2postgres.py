import csv
import re
import sys
from os import listdir
from os.path import isfile, join
from schema import Database, Table, init_db_schema

insert_statements = {}


def write(filename: str, stmt: str): 
    with open(filename, "w") as f:
        f.write(stmt)


def get_all_files(filepath: str) -> list:
    return [join(filepath, f) for f in listdir(filepath) if isfile(join(filepath, f))]


def insert_repr(table: Table, val: dict) -> str:
    return table.get_column(val[0]).insert_repr(val[1])


def replace_comma_with_semi(statement: str) -> str:
    return statement[:-1] + ';'


def parse_csvfiles(db: Database, csvfiles: list, filename: str):
    for csvfile in csvfiles:
        print('parsing csvfile', csvfile)
        base = re.sub(r'.*[/]', '', csvfile)
        table_name = base.split('.')[0]
        table: Table = db.get_table(table_name)
        if table is None:
            continue

        statement = ""

        with open(csvfile, newline='\n') as f:
            reader = csv.DictReader(f)
            insert_prefix = f"INSERT INTO {table_name} ({','.join([k for k in reader.fieldnames])}) VALUES"
            current_statement = insert_prefix
            batch_size = 50000
            for (i, row) in enumerate(reader):
                # batch insert statements for large tables
                if (i % batch_size == 0 and i != 0):
                    statement += f"{replace_comma_with_semi(current_statement)}"
                    current_statement = f"\n\n{insert_prefix}"
                current_statement += f"\n({','.join([insert_repr(table, val) for val in row.items()])}),"

            # replace last comma with a semi colon
            statement += replace_comma_with_semi(current_statement)
            insert_statements[table_name] = statement

    for (i, table) in enumerate(db.insert_order):
        write(f"{i+1}_{table.name}_{filename}.sql", insert_statements[table.name])

db = init_db_schema()
parse_csvfiles(db, get_all_files(sys.argv[1]), sys.argv[2])
