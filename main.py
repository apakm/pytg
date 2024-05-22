from pytg.engine import PYTGEngine

game_engine = PYTGEngine()

game_engine.add_command(
    "help", 
    "Shows a list of available commands.",
    lambda: print("Help command executed.")
)

game_engine.start()