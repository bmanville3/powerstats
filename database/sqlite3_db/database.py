import sqlite3
import pandas as pd
from typing import Dict, Any

DB_FILE = "powerlifting.db"


class DBWrapper:
    def __init__(self, table_name: str, conn: sqlite3.Connection | None = None):
        if conn is None:
            self.conn = sqlite3.connect(DB_FILE)
        else:
            self.conn = conn
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def insert(self, data: Dict[str, Any]) -> None:
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {self.table_name} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))
        self.conn.commit()

    def fetch_head(self, n: int = 5) -> pd.DataFrame:
        query = f"SELECT * FROM {self.table_name} LIMIT ?"
        return pd.read_sql_query(query, self.conn, params=(n,))

    def bulk_insert_from_df(self, df: pd.DataFrame) -> None:
        df.to_sql(self.table_name, self.conn, if_exists="append", index=False)

    def close(self) -> None:
        self.conn.close()


class LifterDB(DBWrapper):
    def __init__(self, conn: sqlite3.Connection | None = None):
        super().__init__("lifters", conn)


class MeetDB(DBWrapper):
    def __init__(self, conn: sqlite3.Connection | None = None):
        super().__init__("meets", conn)


class ResultDB(DBWrapper):
    def __init__(self, conn: sqlite3.Connection | None = None):
        super().__init__("results", conn)


class PowerliftingDatabase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_FILE)
        self.lifter_db = LifterDB(self.conn)
        self.meet_db = MeetDB(self.conn)
        self.result_db = ResultDB(self.conn)
        self.all_dbs: list[DBWrapper] = [self.lifter_db, self.meet_db, self.result_db]

    def close(self) -> None:
        for db in self.all_dbs:
            db.close()


if __name__ == "__main__":
    database = PowerliftingDatabase()
    for db in database.all_dbs:
        n = 10
        print(
            f"Displaying top {n} rows from {db.table_name}:\n{db.fetch_head(n)}\n"
        )
    database.close()
