class Column:
    def __init__(self, name: str, primitive: str, fk_table: str = None,
                 fk_col: str = None, is_pk: bool = False, is_unique: bool = False):
        self.name = name
        self.primitive = primitive
        self.is_pk = is_pk
        self.is_unique = is_unique
        self.fk_table = fk_table
        self.fk_col = fk_col

        if self.fk_table and not self.fk_col:
            self.fk_col = self.name

    def sql_repr(self) -> str:
        sql = f"\t{self.name} {self.primitive}"
        if self.is_pk:
            sql += " primary key"
        if self.is_unique:
            sql += " unique"
        if self.fk_table:
            sql += f" references {self.fk_table}({self.fk_col})"
        return sql

    def insert_repr(self, val: str) -> str:
        if self.primitive == "int" and val == '':
            return "-1"

        if "varchar" in self.primitive:
            x = val.replace("'", "''")
            return f"'{x}'"

        return val


class Table:
    def __init__(self, name: str):
        self.name = name
        self.columns = []

    def get_column(self, name: str) -> Column:
        for c in self.columns:
            if c.name == name:
                return c
        return None

    def add_column(self, column: Column):
        self.columns.append(column)

    def get_pk(self) -> Column:
        for c in self.columns:
            if c.is_pk:
                return c
        return None

    def get_fks(self) -> Column:
        fks = []
        for c in self.columns:
            if c.fk_table is not None:
                fks.append(c)
        return fks


class Database:
    def __init__(self):
        self.tables = []
        self.insert_order = []

    def get_table(self, name: str) -> Table:
        for t in self.tables:
            if t.name == name:
                return t
        return None

    def add_table(self, table: Table):
        self.tables.append(table)

    def build(self, filename: str = None):
        if not filename:
            filename = "0_schema.sql"

        with open(filename, "w") as f:
            for table in self.tables:
                f.write(f"create table {table.name} (\n")
                f.write(",\n".join([c.sql_repr() for c in table.columns]))
                f.write(f"\n);\n")

                fks = table.get_fks()
                for fk in fks:
                    f.write(f"CREATE RULE \"{table.name}_{fk.name}_on_fk_err_ignore\" AS ON INSERT TO \"{table.name}\" WHERE NOT EXISTS (SELECT 1 FROM {fk.fk_table} WHERE {fk.fk_table}.{fk.fk_col}=NEW.{fk.name}) DO INSTEAD NOTHING;\n\n")


def init_db_schema():
    db = Database()

    # routes
    routes_table = Table("routes")
    routes_table.add_column(Column("route_id", "int", is_pk=True))
    routes_table.add_column(Column("agency_id", "int"))
    routes_table.add_column(Column("route_short_name", "varchar(255)"))
    routes_table.add_column(Column("route_long_name", "varchar(255)"))
    routes_table.add_column(Column("route_desc", "varchar(255)"))
    routes_table.add_column(Column("route_type", "varchar(255)"))
    routes_table.add_column(Column("route_url", "varchar(255)"))
    routes_table.add_column(Column("route_color", "varchar(255)"))
    routes_table.add_column(Column("route_text_color", "varchar(255)"))
    db.add_table(routes_table)

    # trips
    trips_table = Table("trips")
    trips_table.add_column(Column("trip_id", "varchar(255)", is_pk=True))
    trips_table.add_column(Column("route_id", "int", fk_table="routes"))
    trips_table.add_column(Column("service_id", "varchar(255)"))
    trips_table.add_column(Column("trip_headsign", "varchar(255)"))
    trips_table.add_column(Column("trip_short_name", "varchar(255)"))
    trips_table.add_column(Column("direction_id", "varchar(255)"))
    trips_table.add_column(Column("shape_id", "varchar(255)"))
    db.add_table(trips_table)

    # stops
    stops_table = Table("stops")
    stops_table.add_column(Column("stop_id", "int", is_pk=True))
    stops_table.add_column(Column("stop_code", "int"))
    stops_table.add_column(Column("stop_name", "varchar(255)"))
    stops_table.add_column(Column("stop_desc", "varchar(255)"))
    stops_table.add_column(Column("stop_lat", "varchar(255)"))
    stops_table.add_column(Column("stop_lon", "varchar(255)"))
    stops_table.add_column(Column("location_type", "varchar(255)"))
    stops_table.add_column(Column("parent_station", "varchar(255)"))
    db.add_table(stops_table)

    # transfers
    transfers_table = Table("transfers")
    transfers_table.add_column(Column("transfer_id", "serial", is_pk=True))
    transfers_table.add_column(Column("from_stop_id", "int", fk_table="stops", fk_col="stop_id"))
    transfers_table.add_column(Column("to_stop_id", "int", fk_table="stops", fk_col="stop_id"))
    transfers_table.add_column(Column("transfer_type", "int"))
    transfers_table.add_column(Column("min_transfer_time", "int"))
    db.add_table(transfers_table)

    # stop_times
    stoptimes_table = Table("stop_times")
    stoptimes_table.add_column(Column("stop_time_id", "serial", is_pk=True))
    stoptimes_table.add_column(Column("trip_id", "varchar(255)", fk_table="trips"))
    stoptimes_table.add_column(Column("arrival_time", "varchar(63)"))
    stoptimes_table.add_column(Column("departure_time", "varchar(63)"))
    stoptimes_table.add_column(Column("stop_id", "int", fk_table="stops"))
    stoptimes_table.add_column(Column("stop_sequence", "int"))
    stoptimes_table.add_column(Column("stop_headsign", "varchar(255)"))
    stoptimes_table.add_column(Column("shape_dist_traveled", "varchar(255)"))
    db.add_table(stoptimes_table)

    # calendar
    calendar_table = Table("calendar")
    calendar_table.add_column(Column("service_id", "int", is_pk=True))
    calendar_table.add_column(Column("monday", "int"))
    calendar_table.add_column(Column("tuesday", "int"))
    calendar_table.add_column(Column("wednesday", "int"))
    calendar_table.add_column(Column("thursday", "int"))
    calendar_table.add_column(Column("friday", "int"))
    calendar_table.add_column(Column("saturday", "int"))
    calendar_table.add_column(Column("sunday", "int"))
    calendar_table.add_column(Column("start_date", "varchar(8)"))
    calendar_table.add_column(Column("end_date", "varchar(8)"))
    db.add_table(calendar_table)

    # calendar_dates
    calendardates_table = Table("calendar_dates")
    calendardates_table.add_column(Column("calendar_date_id", "serial", is_pk=True))
    calendardates_table.add_column(Column("service_id", "int", fk_table="calendar"))
    calendardates_table.add_column(Column("date", "varchar(8)"))
    calendardates_table.add_column(Column("exception_type", "int"))
    db.add_table(calendardates_table)

    # agency
    # agency_table = Table("agency")
    # agency_table.add_column(Column("agency_id", "int"))
    # agency_table.add_column(Column("agency_name", "varchar(255)"))
    # agency_table.add_column(Column("agency_url", "varchar(255)"))
    # agency_table.add_column(Column("agency_timezone", "varchar(15)"))
    # agency_table.add_column(Column("agency_lang", "varchar(4)"))
    # agency_table.add_column(Column("agency_phone", "varchar(15)"))
    # db.add_table(agency_table)

    db.insert_order = [
        routes_table,
        trips_table,
        stops_table,
        transfers_table,
        stoptimes_table,
        calendar_table,
        calendardates_table,
        # agency_table,
    ]

    return db


if __name__ == "__main__":
    db = init_db_schema()
    db.build()
