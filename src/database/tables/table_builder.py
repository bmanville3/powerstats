from enum import Enum, auto


def lowercase_first(string: str) -> str:
    if not string:
        return string
    else:
        return string[0].lower() + string[1:]


def camel_caser(string: str) -> str:
    if not string:
        return string
    string = lowercase_first(string)
    return "".join(
        ["_" + letter.lower() if letter.isupper() else letter for letter in string]
    )


class ColumnBuilder:
    class Type(Enum):
        """SQL data types."""

        NULL = "NULL"
        """The value is a NULL value."""
        INTEGER = "INTEGER"
        """The value is a signed integer, stored in 0, 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value."""
        REAL = "REAL"
        """The value is a floating point value, stored as an 8-byte IEEE floating point number."""
        TEXT = "TEXT"
        """The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE)."""
        BLOB = "BLOB"
        """The value is a blob of data, stored exactly as it was input."""

        def python_type(self) -> str:
            return {
                ColumnBuilder.Type.NULL: "None",
                ColumnBuilder.Type.INTEGER: "int",
                ColumnBuilder.Type.REAL: "float",
                ColumnBuilder.Type.TEXT: "str",
                ColumnBuilder.Type.BLOB: "bytes",
            }[self]

    class Attribute(Enum):
        AUTOINCREMENT = auto()
        NOT_NULL = auto()
        UNIQUE = auto()
        PRIMARY_KEY = auto()

    def __init__(
        self,
        name: str,
        type_: "ColumnBuilder.Type",
        python_variable_name: str | None = None,
    ):
        if not name:
            raise ValueError("Name must be given to column")
        self._name = name
        self._type = type_
        self._attributes: set[ColumnBuilder.Attribute] = set()
        self._python_variable_name = (
            python_variable_name if python_variable_name else camel_caser(self._name)
        )

    def add_attribute(self, attribute: "ColumnBuilder.Attribute") -> "ColumnBuilder":
        self._attributes.add(attribute)
        return self

    def set_python_variable_name(self, python_variable_name: str) -> "ColumnBuilder":
        self._python_variable_name = python_variable_name
        return self

    def build(self) -> str:
        parts = [self._name, self._type.value]
        if ColumnBuilder.Attribute.PRIMARY_KEY in self._attributes:
            parts.append("PRIMARY KEY")
        if ColumnBuilder.Attribute.AUTOINCREMENT in self._attributes:
            parts.append("AUTOINCREMENT")
        if ColumnBuilder.Attribute.NOT_NULL in self._attributes:
            parts.append("NOT NULL")
        if ColumnBuilder.Attribute.UNIQUE in self._attributes:
            parts.append("UNIQUE")
        return " ".join(parts)

    def python_field(self) -> str:
        """
        Gets the corresponding python field.
        For example, "num REAL" -> "num: float | None".
        """
        typ = self._type.python_type()
        if (
            ColumnBuilder.Attribute.NOT_NULL not in self._attributes
            and ColumnBuilder.Attribute.PRIMARY_KEY not in self._attributes
        ):
            typ = f"{typ} | None"
        return f"{self._python_variable_name}: {typ}"


class TableBuilder:
    def __init__(self, name: str, python_class_name: str | None = None):
        if not name:
            raise ValueError("Name must be given to table")
        self._name = name
        self._columns: list[ColumnBuilder] = []
        self._names: set[str] = set()
        self._foreign: dict[str, tuple[str, str]] = {}
        self._if_not_exists = True
        self._python_class_name = (
            python_class_name if python_class_name else self._name.capitalize()
        )

    def add_column(
        self,
        column: ColumnBuilder,
        foreign_table: str | None = None,
        foreign_col: str | None = None,
    ) -> "TableBuilder":
        if column._name in self._names:
            raise ValueError(f"Column {column._name} already in builder")
        self._columns.append(column)
        if foreign_table:
            self._foreign[column._name] = (
                foreign_table,
                foreign_col if foreign_col else column._name,
            )
        return self

    def set_if_not_exists(self, value: bool) -> "TableBuilder":
        self._if_not_exists = value
        return self

    def set_python_class_name(self, name: str) -> "TableBuilder":
        self._python_class_name = name
        return self

    def build_sql(self) -> str:
        if not self._columns:
            raise ValueError("No columns defined for the table.")
        if_clause = "IF NOT EXISTS " if self._if_not_exists else ""
        column_sql = ",\n    ".join(col.build() for col in self._columns)
        foreign_sql = ",\n    ".join(
            f"FOREIGN KEY ({col_name}) REFERENCES {foreign_table}({foreign_col})"
            for col_name, (foreign_table, foreign_col) in self._foreign.items()
        )
        if foreign_sql:
            column_sql = column_sql + ",\n\n    " + foreign_sql
        return f"CREATE TABLE {if_clause}{self._name} (\n    {column_sql}\n);"

    def generate_python_class(self) -> str:
        fields = "\n    ".join(col.python_field() for col in self._columns)
        return f"@dataclass\nclass {self._python_class_name}:\n    {fields}"

    def generate_table_class(self) -> str:
        methods = []
        unique_columns = [
            col
            for col in self._columns
            if ColumnBuilder.Attribute.PRIMARY_KEY in col._attributes
            or ColumnBuilder.Attribute.UNIQUE in col._attributes
        ]
        other_columns = [col for col in self._columns if col not in unique_columns]
        for col in other_columns:
            methods.append(f'''
    def get_by_{col._python_variable_name}(self, value: {col._type.python_type()}) -> list[{self._python_class_name}]:
        return self.get_all_from_attribute("{col._name}", value)''')
            if col._type in {
                ColumnBuilder.Type.REAL,
                ColumnBuilder.Type.INTEGER,
                ColumnBuilder.Type.TEXT,
            }:
                methods.append(f'''
    def get_where_{col._python_variable_name}_ge(self, value: {col._type.python_type()}) -> list[{self._python_class_name}]:
        return self.get_all_from_attributes_with_comparator((("{col._name}", Comparator.GE, value),))

    def get_where_{col._python_variable_name}_le(self, value: {col._type.python_type()}) -> list[{self._python_class_name}]:
        return self.get_all_from_attributes_with_comparator((("{col._name}", Comparator.LE, value),))

    def get_where_{col._python_variable_name}_in_range(self, lower_inclusive: {col._type.python_type()}, upper_inclusive: {col._type.python_type()}) -> list[{self._python_class_name}]:
        return self.get_all_from_attributes_with_comparator((("{col._name}", Comparator.GE, lower_inclusive), ("{col._name}", Comparator.LE, upper_inclusive)))''')
        for col in unique_columns:
            methods.append(f'''
    def get_by_unique_{col._python_variable_name}(self, value: {col._type.python_type()}) -> {self._python_class_name} | None:
        results = self.get_all_from_attribute("{col._name}", value)
        if not results:
            return None
        if len(results) > 1:
            raise ValueError("Multiple results returned for unique query")
        return results[0]''')
        method_str = "\n".join(methods)
        return f'''
class {self._python_class_name}Table(Table[{self._python_class_name}]):
    @classmethod
    def get_create_table_script(cls) -> str:
        return """{self.build_sql()}"""

    @classmethod
    def get_table_name(cls) -> str:
        return "{self._name}"

    @classmethod
    def get_model_class(cls) -> Type[{self._python_class_name}]:
        return {self._python_class_name}
{method_str}'''
