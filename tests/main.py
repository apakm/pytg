import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pytg.engine import PYTGEngine

game_engine = PYTGEngine()

game_engine.add_command(
    "help", 
    "Shows a list of available commands.",
    lambda: print("Help command executed.")
)

game_engine.add_command(
    "exit",
    "Exits the game.",
    game_engine.stop
)

game_engine.start()