# ---------- KEYWORDS --------------


UNIQUE = "unique"
NOT_UNIQUE = "not_unique"

NULLABLE = "nullable"
NOT_NULLABLE = "not_nullable"

UNSPECIFIED = "unspecified"

INTEGER = "integer"
FLOAT = "float"
STRING = "string"
BOOLEAN = "boolean"
MIXED = "mixed"
TYPES_LIST = [INTEGER, FLOAT, STRING, BOOLEAN, MIXED]

TABLE_NAME = "table_name"
PRIMARY_KEY = "primary_key"
FOREIGN_KEY = "foreign_key"
COLUMN_KEYS = "column_keys"

TYPE = "type"
UNIQUENESS = "uniqueness"
NULL = "null"

FAILURE = "failure"
SUCCESS = "success"


# ------------ UTILITIES -------------------


def check_type(obj, typ, nullability):
    if type(obj) == int and typ == INTEGER:
        return True
    elif type(obj) == float and typ == FLOAT:
        return True
    elif type(obj) == str and typ == STRING:
        return True
    elif type(obj) == bool and typ == BOOLEAN:
        return True
    elif typ == MIXED:
        return True
    elif obj == None and nullability:
        return True
    return False

# ------------ SCHEMA RELATED ---------------


schema = {TABLE_NAME: "Students at Cornell University",
          PRIMARY_KEY: ["STUDENT_ID"],
          FOREIGN_KEY: [],
          COLUMN_KEYS: {"STUDENT_ID": {TYPE: STRING,
                                       UNIQUENESS: UNIQUE,
                                       NULL: NOT_NULLABLE},
                        "STUDENT_NAME": {TYPE: STRING,
                                         UNIQUENESS: NOT_UNIQUE,
                                         NULL: NULLABLE},
                        "AGE": {TYPE: INTEGER,
                                UNIQUENESS: NOT_UNIQUE,
                                NULL: NULLABLE},
                        }
          }


class Table:
    """
    Table represents a table
    """

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        self._table = table

    @table.deleter
    def table(self):
        del self._table

    def __init__(self, schema, table, name_to_idx, idx_to_name):
        """
        __init__(self, schema, table) creates a table object with schema schema
        and table table
        """
        self._schema = schema
        self._table = table
        self._name_to_idx = name_to_idx
        self._idx_to_name = idx_to_name

    def insert(self, row):

        # check row length is correct
        if len(row) != len(self._name_to_idx):
            return FAILURE

        # check schema items are of right type including nullable
        schema = self._schema
        column_keys = schema[COLUMN_KEYS]
        idx = 0
        for key in column_keys:
            col_dict = column_keys[key]
            typ = col_dict[TYPE]
            nullability = col_dict[NULL]
            val = row[idx]
            if not check_type(val, typ, nullability):
                return FAILURE
            idx += 1

        # check for uniqueness
        idx = 0
        for key in column_keys:
            col_dict = column_keys[key]
            uniqueness = col_dict[UNIQUENESS]
            if uniqueness == UNIQUE:
                val = row[idx]
                column_idx = self._name_to_idx[key]
                column_data = list(
                    map(lambda row: row[column_idx], self._table))
                if val in column_data:
                    return FAILURE
            idx += 1

        # insertion
        self._table.append(row)

        return SUCCESS


def init_table(schema):
    """
    init_table(schema) creates a table based on the schema given

    RETURNS: table object initialized
    """
    column_keys = schema[COLUMN_KEYS]
    col_names = [key for key in column_keys]
    name_to_idx = {pair[1]: pair[0] for pair in enumerate(col_names)}
    idx_to_name = {pair[0]: pair[1] for pair in enumerate(col_names)}
    table = []
    return Table(schema, table, name_to_idx, idx_to_name)


def insert_table(table_obj, row):
    table_obj.insert(row)
