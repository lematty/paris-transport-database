class Column:
    def __init__(self, name: str, primitive: str, foreign_key_table: str = None,
                 foreign_key_column: str = None, is_primary_key: bool = False, is_unique: bool = False):
        self.name = name
        self.primitive = primitive
        self.is_primary_key = is_primary_key
        self.is_unique = is_unique
        self.foreign_key_table = foreign_key_table
        self.foreign_key_column = foreign_key_column

        if self.foreign_key_table and not self.foreign_key_column:
            self.foreign_key_column = self.name

    def sql_repr(self) -> str:
        sql = f"\t{self.name} {self.primitive}"
        if self.is_primary_key:
            sql += " primary key"
        if self.is_unique:
            sql += " unique"
        if self.foreign_key_table:
            sql += f" references {self.foreign_key_table}({self.foreign_key_column})"
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
        for column in self.columns:
            column: Column
            if column.is_primary_key:
                return column
        return None

    def get_foreign_keys(self) -> Column:
        foreign_keys = []
        for column in self.columns:
            column: Column
            if column.foreign_key_table is not None:
                foreign_keys.append(column)
        return foreign_keys


class Database:
    def __init__(self):
        self.tables = []
        self.insert_order = []

    def get_table(self, name: str) -> Table:
        for table in self.tables:
            table: Table
            if table.name == name:
                return table
        return None

    def add_table(self, table: Table):
        self.tables.append(table)

    def build(self, filename: str = None):
        if not filename:
            filename = "0_schema.sql"

        with open(filename, "w") as f:
            for table in self.insert_order:
                table: Table
                f.write(f"CREATE TABLE {table.name} (\n")
                f.write(",\n".join([column.sql_repr() for column in table.columns]))
                f.write(f"\n);\n")

                foreign_keys = table.get_foreign_keys()
                for foreign_key in foreign_keys:
                    foreign_key: Column
                    f.write(f"CREATE RULE \"{table.name}_{foreign_key.name}_on_foreign_key_err_ignore\" AS ON INSERT TO \"{table.name}\" WHERE NOT EXISTS (SELECT 1 FROM {foreign_key.foreign_key_table} WHERE {foreign_key.foreign_key_table}.{foreign_key.foreign_key_column}=NEW.{foreign_key.name}) DO INSTEAD NOTHING;\n\n")


def init_db_schema():
    db = Database()

    # agency
    agency_table = Table("agency")
    agency_table.add_column(Column("agency_id", "varchar(255)", is_primary_key=True))
    agency_table.add_column(Column("agency_name", "varchar(255)"))
    agency_table.add_column(Column("agency_url", "varchar(255)"))
    agency_table.add_column(Column("agency_timezone", "varchar(15)"))
    agency_table.add_column(Column("agency_lang", "varchar(4)"))
    agency_table.add_column(Column("agency_phone", "varchar(15)"))
    agency_table.add_column(Column("agency_email", "varchar(15)"))
    db.add_table(agency_table)

    # calendar
    calendar_table = Table("calendar")
    calendar_table.add_column(Column("service_id", "varchar(255)", is_primary_key=True))
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
    calendardates_table.add_column(Column("calendar_date_id", "serial", is_primary_key=True))
    calendardates_table.add_column(Column("service_id", "varchar(255)", foreign_key_table="calendar"))
    calendardates_table.add_column(Column("date", "varchar(8)"))
    calendardates_table.add_column(Column("exception_type", "int"))
    db.add_table(calendardates_table)

    # pathways
    pathways_table = Table("pathways")
    pathways_table.add_column(Column("pathway_id", "varchar(255)", is_primary_key=True))
    pathways_table.add_column(Column("from_stop_id", "varchar(255)", foreign_key_table="stops", foreign_key_column="stop_id"))
    pathways_table.add_column(Column("to_stop_id", "varchar(255)", foreign_key_table="stops", foreign_key_column="stop_id"))
    pathways_table.add_column(Column("pathway_mode", "varchar(15)"))
    pathways_table.add_column(Column("is_bidirectional", "int"))
    pathways_table.add_column(Column("length", "varchar(15)"))
    pathways_table.add_column(Column("traversal_time", "int"))
    pathways_table.add_column(Column("stair_count", "varchar(15)"))
    pathways_table.add_column(Column("max_slope", "varchar(15)"))
    pathways_table.add_column(Column("min_width", "varchar(15)"))
    pathways_table.add_column(Column("signposted_as", "varchar(15)"))
    pathways_table.add_column(Column("reversed_signposted_as", "varchar(15)"))
    db.add_table(pathways_table)

    # routes
    routes_table = Table("routes")
    routes_table.add_column(Column("route_id", "varchar(255)", is_primary_key=True))
    routes_table.add_column(Column("agency_id", "varchar(255)", foreign_key_table="agency"))
    routes_table.add_column(Column("route_short_name", "varchar(255)"))
    routes_table.add_column(Column("route_long_name", "varchar(255)"))
    routes_table.add_column(Column("route_desc", "varchar(255)"))
    routes_table.add_column(Column("route_type", "int"))
    routes_table.add_column(Column("route_url", "varchar(255)"))
    routes_table.add_column(Column("route_color", "varchar(255)"))
    routes_table.add_column(Column("route_text_color", "varchar(255)"))
    routes_table.add_column(Column("route_sort_order", "varchar(255)"))
    db.add_table(routes_table)

    # stops
    stops_table = Table("stops")
    stops_table.add_column(Column("stop_id", "varchar(255)", is_primary_key=True))
    stops_table.add_column(Column("stop_code", "int"))
    stops_table.add_column(Column("stop_name", "varchar(255)"))
    stops_table.add_column(Column("stop_desc", "varchar(255)"))
    stops_table.add_column(Column("stop_lon", "varchar(255)"))
    stops_table.add_column(Column("stop_lat", "varchar(255)"))
    stops_table.add_column(Column("zone_id", "int"))
    stops_table.add_column(Column("stop_url", "varchar(255)"))
    stops_table.add_column(Column("location_type", "varchar(255)"))
    stops_table.add_column(Column("parent_station", "varchar(255)"))
    stops_table.add_column(Column("stop_timezone", "varchar(255)"))
    stops_table.add_column(Column("level_id", "varchar(255)"))
    stops_table.add_column(Column("wheelchair_boarding", "int"))
    stops_table.add_column(Column("platform_code", "varchar(255)"))
    db.add_table(stops_table)

    # stop_extensions
    stop_extensions_table = Table("stop_extensions")
    stop_extensions_table.add_column(Column("stop_extension_id", "serial", is_primary_key=True))
    stop_extensions_table.add_column(Column("object_id", "varchar(255)", foreign_key_column="stop_id"))
    stop_extensions_table.add_column(Column("object_system", "varchar(255)"))
    stop_extensions_table.add_column(Column("object_code", "varchar(255)"))
    db.add_table(stop_extensions_table)

    # stop_times
    stoptimes_table = Table("stop_times")
    stoptimes_table.add_column(Column("stop_time_id", "serial", is_primary_key=True))
    stoptimes_table.add_column(Column("trip_id", "varchar(255)", foreign_key_table="trips"))
    stoptimes_table.add_column(Column("arrival_time", "varchar(63)"))
    stoptimes_table.add_column(Column("departure_time", "varchar(63)"))
    stoptimes_table.add_column(Column("stop_id", "varchar(255)", foreign_key_table="stops"))
    stoptimes_table.add_column(Column("stop_sequence", "int"))
    stoptimes_table.add_column(Column("pickup_type", "varchar(255)"))
    stoptimes_table.add_column(Column("drop_off_type", "varchar(255)"))
    stoptimes_table.add_column(Column("local_zone_id", "varchar(255)"))
    stoptimes_table.add_column(Column("stop_headsign", "varchar(255)"))
    stoptimes_table.add_column(Column("timepoint", "varchar(255)"))
    db.add_table(stoptimes_table)

    # transfers
    transfers_table = Table("transfers")
    transfers_table.add_column(Column("transfer_id", "serial", is_primary_key=True))
    transfers_table.add_column(Column("from_stop_id", "varchar(255)", foreign_key_table="stops", foreign_key_column="stop_id"))
    transfers_table.add_column(Column("to_stop_id", "varchar(255)", foreign_key_table="stops", foreign_key_column="stop_id"))
    transfers_table.add_column(Column("transfer_type", "int"))
    transfers_table.add_column(Column("min_transfer_time", "int"))
    db.add_table(transfers_table)

    # trips
    trips_table = Table("trips")
    trips_table.add_column(Column("trip_id", "varchar(255)", is_primary_key=True))
    trips_table.add_column(Column("route_id", "varchar(255)", foreign_key_table="routes"))
    trips_table.add_column(Column("service_id", "varchar(255)", foreign_key_table="calendar"))
    trips_table.add_column(Column("trip_headsign", "varchar(255)"))
    trips_table.add_column(Column("trip_short_name", "varchar(255)"))
    trips_table.add_column(Column("direction_id", "varchar(255)"))
    trips_table.add_column(Column("block_id", "varchar(255)"))
    trips_table.add_column(Column("shape_id", "varchar(255)"))
    trips_table.add_column(Column("wheelchair_accessible", "int"))
    trips_table.add_column(Column("bikes_allowed", "int"))
    db.add_table(trips_table)

    db.insert_order = [
        agency_table,
        routes_table,
        stops_table,
        transfers_table,
        calendar_table,
        calendardates_table,
        trips_table,
        stoptimes_table,
        pathways_table,
        stop_extensions_table,
    ]

    return db


if __name__ == "__main__":
    db = init_db_schema()
    db.build()
