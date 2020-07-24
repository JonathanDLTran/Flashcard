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


# ------------ SCHEMA RELATED ---------------


schema = {TABLE_NAME: "Students at Cornell University",
          PRIMARY_KEY: ["STUDENT_ID"],
          FOREIGN_KEY: [],
          COLUMN_KEYS: {"STUDENT_ID": {"type": STRING,
                                       "uniqueness": UNIQUE,
                                       "null": NOT_NULLABLE},
                        "STUDENT_NAME": {"type": STRING,
                                         "uniqueness": NOT_UNIQUE,
                                         "null": NULLABLE},
                        "AGE": {"type": INTEGER,
                                "uniqueness": NOT_UNIQUE,
                                "null": NULLABLE},
                        }
          }


class Table:
    """
    Table represents a table
    """

    def __init__(self, schema):
        """
        __init__(self, schema) creates a table object with schema schema
        """
        self.schema = schema


def init_table(schema):
    """
    init_table(schema) creates a table based on the schema given 
    """
