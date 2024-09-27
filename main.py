from src.game import Game
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from src.rendering import clear

play_again_msg = f"""Play again?:
  0. (default) Exit.
  1. Play again.

Selection: """

cfg_selection_msg = f"""Choose Config Type
  0. (default) Manual Config
  1. Human vs Human (3x3, 3)
  2. Human vs DumBot (3x3, 3)
  3. Human vs EasyBot (3x3, 3)
  4. Human vs MedBot(3x3, 3)
  5. Load config file
	
Selection: """


if __name__ == "__main__":
	while True:
		clear()
		cfg_type = input(cfg_selection_msg)


		g = Game()

		if cfg_type == '1':
			cfg_status = g.load_config('game-configs/human-human-3-3-3.json')
		
		elif cfg_type == '2':
			cfg_status = g.load_config('game-configs/human-dumbot-3-3-3.json')

		elif cfg_type == '3':
			cfg_status = g.load_config('game-configs/human-medbot-3-3-3.json')
		
		elif cfg_type == '4':
			cfg_status = g.load_config('game-configs/human-medbot-3-3-3.json')

		elif cfg_type == '5':
			root = Tk()
			Tk().withdraw()
			fn = askopenfilename()
			root.destroy()
			cfg_status = g.load_config(fn)

		else:
			cfg_status = g.config()

		
		if cfg_status >= 0:
			g.play()
			print(g.players)
			exit()
			play_again = input(play_again_msg)
			if play_again == '1':
				continue
			else:
				break
		else:
			print("Failed to load config")