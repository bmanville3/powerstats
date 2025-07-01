"""
Module containing access points to the main SQLite database.

All access to the database should be done through this module.
"""

import logging
import sqlite3
from typing import Any, Sequence

from src.utils.utils import find_dir

logger = logging.getLogger(__name__)


class Database:
    """
    An object that holds a connection to a database.
    If no database is specified, connects to the MAIN database

    Args:
        server (str | None): The database to connect to.
        backup (str | None): The backup database to write to upon closing.
    """

    def __init__(self, server: str | None = None, backup: str | None = None) -> None:
        if server is None:
            server_path = (find_dir("data") / "sqlite") / "powerlifting.db"
            if not server_path.exists():
                raise FileNotFoundError(
                    f"Could not find database at {server_path}. Is it there?"
                )
            server = str(server_path.absolute())
        self.server = server
        self.backup = backup
        logger.info("Establishing a connection to %s...", self.server)
        self._connection = sqlite3.connect(self.server)
        self._connection.execute("PRAGMA foreign_keys = ON")
        logger.info("Connection to %s has been established", self.server)

    def execute(
        self, sql: str, params: dict[str, Any] | Sequence[Any] = ()
    ) -> list[Any] | None:
        """
        Execute an sql statement on the database. Wrapper for Connection.execute(sql, parameters).
        Commit is ALWAYS called after executing the command.

        To bind data to sql, please use '?' in the string as a placeholder
        and pass the data into params.

        Args:
            sql (str): Statement to run on the database.
            params (dict[str, Any] | Sequence[Any]): Params to pass to Cursor.execute().
                                            If named placedholders are used, pass a dict[str, Any].
                                            Else, use a sequence for the '?' placeholders.

        Returns:
            list[Any] | None: Result of running the statement and
                                calling fetchall() on the returned cursor.
        """
        result = self.execute_no_commit(sql, params)
        self._connection.commit()
        return result

    def execute_no_commit(
        self, sql: str, params: dict[str, Any] | Sequence[Any] = ()
    ) -> list[Any] | None:
        """
        Execute an sql statement on the database. Wrapper for Connection.execute(sql, parameters).
        Commit is NOT called after executing the command.

        To bind data to sql, please use '?' in the string as a placeholder
        and pass the data into params.

        Args:
            sql (str): Statement to run on the database.
            params (dict[str, Any] | Sequence[Any]): Params to pass to Cursor.execute().
                                            If named placedholders are used, pass a dict[str, Any].
                                            Else, use a sequence for the '?' placeholders.

        Returns:
            list[Any] | None: Result of running the statement
                                and calling fetchall() on the returned cursor.
        """
        logger.debug("Input to database: %s\tParams to database: %s", sql, params)
        cursor = self._connection.execute(sql, params)
        logger.debug(
            "%s rows affected by %s statement",
            cursor.rowcount,
            sql.split(maxsplit=1)[0] if " " in sql else sql,
        )
        return cursor.fetchall()

    def close(self) -> None:
        """
        Closes the database connection.
        """
        logger.debug("Flushing all changes to %s...", self.server)
        self._connection.commit()
        logger.info("Closing %s connection...", self.server)
        if self.backup is not None:
            logger.info("Backing up to %s first...", self.backup)
            backup_connection = sqlite3.connect(self.backup)
            self._connection.backup(backup_connection)
            backup_connection.close()
            logger.info(
                "%s has been backed up at %s. Closing now...", self.server, self.backup
            )
        self._connection.close()
        logger.info("The connection to %s has been closed", self.server)
