import time
import sqlite3

class PYTGCommand:
    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback

class PYTGEngine:
    def __init__(self):
        self.game_name = "PYTG Test Game"
        self.state = None
        self.is_running = False
        self.player = None
        self.commands: dict = {}
        self.events = None
        self.world = None
        self.db = sqlite3.connect(f'data/{self.game_name.replace(" ", "_")}.db')
        self.__init_db()

    def __init_db(self):
        """
            Initializes the database for the game. (private method)
        """
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

    def setup(self, player, world, initial_state):
        """
            Sets up the game engine, taking in the player instance, world instance and the starting state of the game.
        """
        self.state = initial_state
        self.player = player
        self.world = world

    def start(self):
        """
            Starts the main game loop.
            Should be called last after setting up the game engine.
        """
        self.is_running = True
        self.main_loop()

    def stop(self):
        """
            Stops the main game loop.
        """
        self.is_running = False

    def __process_command(self, command):
        """
            Processes a command.
        """
        if command in self.commands:
            self.commands[command].callback()
        else:
            print(f"Command '{command}' not found.")

    def main_loop(self):
        while self.is_running:
            command = input("> ")
            self.__process_command(command)

    def add_command(self, name, description, callback):
        """
            Adds a command to the game engine.
        """
        self.commands[name] = PYTGCommand(name, description, callback)