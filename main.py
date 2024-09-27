from src.game import Game
import tkinter as tkinter
from tkinter import filedialog
from src.rendering import clear

play_again_msg = f"""Play again?:
  0. (default) Exit.
  1. Play again.

Selection: """

cfg_selection_msg = f"""Choose Config Type
  0. (default) Manual Config
  1. Human vs Human (3x3, 3)
  2. Human vs DumBot (3x3, 3)
  3. Load config file
	
Selection: """

if __name__ == "__main__":
	while True:
		clear()
		cfg_type = int(input(cfg_selection_msg))


		g = Game()

		if cfg_type == 0:
			cfg_status = g.config()

		if cfg_type == 1:
			cfg_status = g.load_config('game-configs/human-human-3-3-3.json')
		
		if cfg_type == 2:
			cfg_status = g.load_config('game-configs/human-dumbot-3-3-3.json')

		if cfg_type == 3:
			fn = filedialog.askopenfilename(title="Select config file", filetypes=[("JSON file", ('*.json')), ("All files", "*.*")])
			cfg_status = g.load_config(fn)

		
		if cfg_status >= 0:
			g.play()
			play_again = input(play_again_msg)
			if play_again == 1:
				continue
			else:
				break
		else:
			print("Failed to load config")