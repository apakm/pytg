import time
import os
import sys

class PYTGStateManager:
    def __init__(self, db, mode):
        self.db = db
        self.mode = mode
        self.__init_db()

    def __init_db(self):
        """
            Initializes the database for the game. (private method)
        """
        if self.mode == "sqlite":
            query = """
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                health INTEGER,
                max_health INTEGER,
                attack INTEGER,
                defense INTEGER,
                gold INTEGER,
                experience INTEGER
            );

            CREATE TABLE IF NOT EXISTS world (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                value INTEGER
            );

            CREATE TABLE IF NOT EXISTS player_items (
                item_id INTEGER,
                player_id INTEGER,
                FOREIGN KEY (item_id) REFERENCES items(id),
                FOREIGN KEY (player_id) REFERENCES player(id)
            );
            """

            self.db.executescript(query)
            self.db.commit()
        elif self.mode == "ini":
            if os.path.exists(self.db):
                return
            else:
                with open(self.db, "w") as inifile:
                    inifile.write("[player]\n")

