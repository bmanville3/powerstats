"""
Module containing the Table class, which is an abstract base class for
all tables in the database. It provides methods for inserting, querying,
updating, and deleting records in the database.
"""

import logging
import sqlite3
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Generic, Type, TypeVar

if TYPE_CHECKING:
    from database.database import Database

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Comparator(Enum):
    EQ = "="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    LIKE = "LIKE"
    IN = "IN"


class Table(ABC, Generic[T]):
    """
    A table in the database.

    Args:
        database (Database): Database object to insert statements into.
    """

    def __init__(self, database: "Database"):
        self.database = database

    @classmethod
    @abstractmethod
    def get_create_table_script(cls) -> str:
        """
        Get the SQL script to create the table.

        Returns:
            str: A runnable sql statement that creates the table if it does not exist.
        """

    @classmethod
    @abstractmethod
    def get_table_name(cls) -> str:
        """
        Get the name of the table in the database.

        Returns:
            str: The name of the table in the database.
        """

    @classmethod
    @abstractmethod
    def get_model_class(cls) -> Type[T]:
        """
        Get the class of the model stored in the table.

        Returns:
            Type[T]: The class of the model stored in the table.
        """

    def seed(self) -> None:
        """
        Fills the database with initial values (if there are initial values to add).
        """

    def get_by_id(self, id_: int) -> T | None:
        """
        Args:
            id_ (int): Id of the object.

        Returns:
            T | None: A new object instantiated from the table.
                        Returns None if the id is not found in the table.
        """
        table_name = self.get_table_name()
        row = self.database.execute_no_commit(
            f"SELECT * FROM {table_name} WHERE id = ?", (id_,)
        )
        logger.debug("Got %s from %s in database", row, table_name)
        if row is None or len(row) == 0:
            return None
        return self.get_model_class()(*row[0])

    def delete(self, id_: int) -> bool:
        """
        Args:
            id_ (int): Id of the object to delete from the table.

        Returns:
            bool: True if successful. Otherwise, it returns False.
        """
        table_name = self.get_table_name()
        try:
            self.database.execute(f"DELETE FROM {table_name} WHERE id = ?", (id_,))
            logger.debug("Successfully deleted id = %s from %s", id_, table_name)
            return True
        except sqlite3.IntegrityError as ie:
            logger.exception(
                "Failed to delete id = %s from %s. Exception: %s", id_, table_name, ie
            )
            return False

    def get_all(self) -> list[T]:
        """
        Get all objects in the table.

        Returns:
            list[T]: A list of all found objects in the table.
        """
        table_name = self.get_table_name()
        clazz = self.get_model_class()
        rows = self.database.execute_no_commit(f"SELECT * FROM {table_name}")
        ret_list = [clazz(*row) for row in rows] if rows else []
        logger.debug(
            "Queried %s objects of type %s from the %s table",
            len(ret_list),
            clazz.__name__,
            table_name,
        )
        return ret_list

    def get_all_from_attribute(
        self, attribute_name: str, attribute_value: Any
    ) -> list[T]:
        """
        Args:
            attribute_name (str): Name of the attribute to query from.
            attribute_value (Any): The value to query for.

        Returns:
            list[T]: A list of all found objects in the table.
        """
        return self.get_all_from_attributes((attribute_name,), (attribute_value,))

    def get_all_from_attributes(
        self, attribute_names: tuple[str, ...], attribute_values: tuple[Any, ...]
    ) -> list[T]:
        """
        Args:
            attribute_names (tuple[str, ...]): List of attribute names (column names).
            attribute_values (tuple[Any, ...]): List of values to query for
                                                each attribute.

        Returns:
            list[T]: A list of all found objects in the table.
        """
        if len(attribute_names) != len(attribute_values):
            logger.error(
                "Number of attributes=%s and values=%s do not match.",
                len(attribute_names),
                len(attribute_values),
            )
            return []

        table_name = self.get_table_name()
        clazz = self.get_model_class()

        conditions = " AND ".join([f"{name} = ?" for name in attribute_names])
        query = f"SELECT * FROM {table_name} WHERE {conditions}"

        rows = self.database.execute_no_commit(query, attribute_values)
        ret_list = [clazz(*row) for row in rows] if rows else []
        logger.debug(
            "Queried %s objects of type %s from the %s table where %s",
            len(ret_list),
            clazz.__name__,
            table_name,
            conditions,
        )
        return ret_list

    def get_all_from_attributes_with_comparator(
        self,
        selection: tuple[tuple[str, Comparator, Any], ...],
    ) -> list[T]:
        """
        Query rows based on attribute names, values, and comparators.

        Args:
            selection (tuple[tuple[str, Comparator, Any], ...]):
                    A tuple of triples containing the column name,
                    the comparator to use, and the value to compare to.

        Returns:
            list[T]: Matching objects.
        """
        if len(selection) == 0:
            return []

        table_name = self.get_table_name()
        clazz = self.get_model_class()

        conditions = []
        sql_values = []

        for name, comp, value in selection:
            if comp == Comparator.IN:
                placeholders = ", ".join("?" for _ in value)
                conditions.append(f"{name} IN ({placeholders})")
                sql_values.extend(value)
            else:
                conditions.append(f"{name} {comp.value} ?")
                sql_values.append(value)

        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"

        rows = self.database.execute_no_commit(query, tuple(sql_values))
        ret_list = [clazz(*row) for row in rows] if rows else []

        logger.debug(
            "Queried %s objects of type %s from %s where %s",
            len(ret_list),
            clazz.__name__,
            table_name,
            where_clause,
        )
        return ret_list

    def add(
        self, attribute_names: tuple[str, ...], attribute_values: tuple[Any, ...]
    ) -> bool:
        """
        Inserts a new entry into the table.

        Args:
            attribute_names (tuple[str, ...]): Tuple of attribute (column) names.
            attribute_values (tuple[Any, ...]): Tuple of values corresponding to
                                                attribute names.

        Returns:
            bool: True if the entry was successfully added, False otherwise.
        """
        if len(attribute_names) != len(attribute_values):
            logger.error(
                "Number of attributes (%s) and values (%s) do not match.",
                len(attribute_names),
                len(attribute_values),
            )
            return False

        table_name = self.get_table_name()
        columns = ", ".join(attribute_names)
        placeholders = ", ".join("?" for _ in attribute_names)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.database.execute(query, attribute_values)
            logger.debug(
                "Inserted into %s (%s): %s", table_name, columns, attribute_values
            )
            return True
        except sqlite3.IntegrityError as ie:
            logger.debug("Integrity error while inserting into %s: %s", table_name, ie)
            return False

    def update(
        self,
        attribute_names: tuple[str, ...],
        attribute_values: tuple[Any, ...],
        condition_names: tuple[str, ...],
        condition_values: tuple[Any, ...],
    ) -> bool:
        """
        Updates rows in the table based on one or more conditions.

        Args:
            attribute_names (tuple[str, ...]): Column names to update.
            attribute_values (tuple[Any, ...]): New values corresponding to the columns.
            condition_names (tuple[str, ...]): Column names for WHERE clause.
            condition_values (tuple[Any, ...]): Values to match in the WHERE clause.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if len(attribute_names) != len(attribute_values):
            logger.error(
                "Mismatched attribute names (%s) and values (%s)",
                len(attribute_names),
                len(attribute_values),
            )
            return False
        if len(condition_names) != len(condition_values):
            logger.error(
                "Mismatched condition names (%s) and values (%s)",
                len(condition_names),
                len(condition_values),
            )
            return False

        table_name = self.get_table_name()
        set_clause = ", ".join([f"{name} = ?" for name in attribute_names])
        where_clause = " AND ".join([f"{name} = ?" for name in condition_names])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        params = attribute_values + condition_values

        try:
            self.database.execute(query, params)
            logger.debug(
                "Updated %s table. Set (%s) to (%s) where (%s) = (%s)",
                table_name,
                ", ".join(attribute_names),
                attribute_values,
                ", ".join(condition_names),
                condition_values,
            )
            return True
        except sqlite3.IntegrityError as ie:
            logger.exception(
                "Failed to update %s table with %s: %s", table_name, where_clause, ie
            )
            return False

    def get_head(self, n: int = 5) -> list[T]:
        table_name = self.get_table_name()
        clazz = self.get_model_class()
        rows = self.database.execute_no_commit(f"SELECT * FROM {table_name} LIMIT {n}")
        ret_list = [clazz(*row) for row in rows] if rows else []
        logger.debug(
            "Queried %s objects of type %s from the %s table",
            len(ret_list),
            clazz.__name__,
            table_name,
        )
        return ret_list
