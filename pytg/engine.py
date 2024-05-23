import time
import sqlite3
from pytg.state import PYTGStateManager

class PYTGMissingSetupError(Exception):
    def __init__(self, message="PYTGEngine is not set up."):
        self.message = message
        super().__init__(self.message)

class PYTGUknownStateModeError(Exception):
    def __init__(self, message="Unknown state mode."):
        self.message = message
        super().__init__(self.message)

class PYTGDuplicateCommandError(Exception):
    def __init__(self, message="Command already exists."):
        self.message = message
        super().__init__(self.message)

class PYTGCommand:
    def __init__(self, name, description, callback):
        self.name = name
        self.description = description
        self.callback = callback

class PYTGEngine:
    STATE_MODE_SQLITE = "sqlite"
    STATE_MODE_INI = "ini"

    
    def __init__(self, game_name="PYTG Test Game", cursor="> ", state_mode=STATE_MODE_SQLITE):
        """
            Initializes the game engine.
        """
        self.game_name = game_name
        self.state = None
        self.is_running = False
        self.player = None
        self.commands: dict = {}
        self.events = None
        self.world = None
        self.cursor = cursor
        self.state_mode = state_mode
        if self.state_mode == PYTGEngine.STATE_MODE_SQLITE:
            self.db = sqlite3.connect(f"{self.game_name}.db")
        elif self.state_mode == PYTGEngine.STATE_MODE_INI:
            self.file = f"{self.game_name}.ini"
        else:
            raise PYTGUknownStateModeError()
        self.state_manager = PYTGStateManager(self.db if self.db else self.file, self.state_mode)

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
            command = input(f"{self.cursor} ")
            self.__process_command(command)

    def add_command(self, name, description, callback):
        """
            Adds a command to the game engine.
        """
        if name in self.commands:
            raise PYTGDuplicateCommandError()
        else:
            self.commands[name] = PYTGCommand(name, description, callback)