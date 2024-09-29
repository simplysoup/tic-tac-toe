from tkinter import Tk, Menu, filedialog, Button
from src.game import Game

default_configs = {
    "Human vs Human (3x3, 3)": 'game-configs\human-human-3-3-3.json',
    "Human vs DumBot (3x3, 3)": 'game-configs\human-dumbot-3-3-3.json',
    "Human vs EasyBot (3x3, 3)": 'game-configs\human-easybot-3-3-3.json',
    "Human vs MedBot (3x3, 3)": 'game-configs\human-medbot-3-3-3.json',
    "Human vs HardBot (3x3, 3)": 'game-configs\human-hardbot-3-3-3.json',
}


current_game = None

def load_previous():
    load_from_config('game-configs/previous.json')

def load_from_config(fn):
    global current_game
    if current_game:
        current_game.quit_game()
    g = Game()
    cfg_status = g.load_config(fn)
    if cfg_status >= 0:
        current_game = g
        current_game.save_config('game-configs/previous.json')
        game_window = Tk()
        game_window.title("Tic Tac Toe")
        g.play_gui(game_window)
        #current_game.play()
    else:
        print("Failed to load config")

def load_config_from_file():
    global current_game
    if current_game:
        current_game.quit_game()
    filename = filedialog.askopenfilename()
    if filename:
        load_from_config(filename)

def manual_config():
    global current_game
    if current_game:
        current_game.quit_game()
    g = Game()
    config_window = Tk()
    cfg_status = g.config(config_window)
    config_window.destroy()
    if cfg_status >= 0:
        current_game = g
        current_game.save_config('game-configs/previous.json')
        game_window = Tk()
        game_window.title("Tic Tac Toe")
        g.play_gui(game_window)
    else:
        print("Failed to load config")

def exit_program():
  menu_window.destroy()

menu_window = Tk()
menu_window.title("Tic-Tac-Toe")

buttons = {}

for k, v in default_configs.items():
    buttons[k] = Button(menu_window, text=k, command=lambda v=v: load_from_config(v))
    buttons[k].pack(pady=10, padx=10)

menubar = Menu(menu_window)

config_menu = Menu(menubar, tearoff=0)
config_menu.add_command(label="Manual Config", command=manual_config)
config_menu.add_command(label="Load config file", command=load_config_from_file)
config_menu.add_command(label="Load previous", command=load_previous)


menubar.add_cascade(label="Config", menu=config_menu)
menubar.add_command(label="Exit", command=exit_program)

menu_window.config(menu=menubar)
menu_window.mainloop()