from src.player import *
from src.board import *
from src.rendering import clear


import pickle
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, Menu




default_player_types = {
    "Player": Player,
    "Human": Human,
    "DumBot": DumBot,
    "EasyBot": EasyBot,
    "MediumBot": MediumBot,
    "HardBot": HardBot,
}




def load_from_pickle():
    filename = filedialog.askopenfilename()
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Pickle file not found.")
        return None


class Game:
    def __init__(self, x: int=3, y: int=3, n: int=3, players: list=[Player('Human', 'X'), DumBot('Random', 'O')]):
        self.board = Board2D(x, y, n, players[0].symbol, players[1].symbol, 0)
        self.players = players
        self.curr_player = 0
        self.quit=False


    def quit_game(self):
        self.quit = True


    def play(self):
        player1 = self.players[0]
        player2 = self.players[1]
        players = [player1, player2]
        board = self.board
        while not self.quit:
            player = players[board.curr_player]
            clear()
            print(board)
            valid_move = -1
            while valid_move < 0:
                print(f'{player.name} to move:', end=' ')
                move = player.move(board)
                print(move + '\n')
                move = move.split(' ')
                if len(move) != 2:
                    print('Move must be two numbers')
                    continue
                valid_move = board.make_move(move[0], move[1])
                if valid_move > 0:
                    print(error_codes[valid_move])


            if board.check_win(player.symbol):
                clear()
                print(board)
                print(f'{player.name} Wins!')
                with open('log.txt', 'a+') as f:
                    f.write(f'{player.name} Wins')
                    f.write(str(board))
                    f.close()
                break
           
            if '-' not in board.state:
                clear()
                print(board)
                print('Tie!')
                with open('log.txt', 'a+') as f:
                    f.write('Tie')
                    f.write(str(board))
                    f.close()
                break


    def play_gui(self, root):
        player1 = self.players[0]
        player2 = self.players[1]
        players = [player1, player2]
        board = self.board
        awaiting_human_input = False


        def button_click(row, col):
            nonlocal awaiting_human_input
            if awaiting_human_input:
                valid_move = board.make_move(str(row), str(col))
                if valid_move < 0:
                    board.curr_player = 1 - board.curr_player
                else:
                    update_grid()
                    check_end()
                    awaiting_human_input = False


        def create_grid(board):
            grid_frame = tk.Frame(root)
            grid_frame.pack()
            buttons = []
            for i in range(board.x):
                row = []
                for j in range(board.y):
                    index = board.index_from_sq(i, j)
                    button = tk.Button(grid_frame, text=board.state[index], width=5, height=2,
                                    command=lambda row=i, col=j: button_click(row, col))
                    button.grid(row=i, column=j)
                    row.append(button)
                buttons.append(row)
            return buttons
       
        def end_game():
            update_grid()
            self.quit_game()
            disable_buttons()
            awaiting_human_input = True
            return


       
        def check_end():
            if board.check_win(players[1-board.curr_player].symbol):
                print(f"{players[1-board.curr_player].name} Wins!")
                end_game()
            elif board.check_draw():
                print("Draw.")
                end_game()
               
       
        def disable_buttons():
                board.curr_player = -1
                for row in buttons:
                    for button in row:
                        button.config(state=tk.DISABLED)
       
        def update_grid():
            for i in range(board.x):
                for j in range(board.y):
                    index = board.index_from_sq(i, j)
                    buttons[i][j].config(text=board.state[index])
       
        def game_loop():
            if self.quit: return
            nonlocal awaiting_human_input
            update_grid()
            if players[board.curr_player].type in ['human', 'player']:
                awaiting_human_input = True
            if players[board.curr_player].type in ['bot']:
                if not awaiting_human_input and not self.quit:
                    move = players[board.curr_player].move(board)
                    move = move.split(' ')
                    valid_move = board.make_move(move[0], move[1])
                    if valid_move < 0:
                        board.curr_player = 1 - board.curr_player
                    else:
                        update_grid()
                        check_end()
            root.after(10, game_loop)
       
        buttons = create_grid(board)
        root.title(f'{self.players[0].name} ({self.players[0].__class__.__name__}) vs. {self.players[1].name} ({self.players[1].__class__.__name__})')
        game_loop()
        root.mainloop()


    def load_config(self, fn):
        with open(fn) as cfg_file:
            cfg =  json.load(cfg_file)
            players = cfg['players']
            p1, p2 = players


            if p1['player_type'] in default_player_types:
                player1 = default_player_types[p1['player_type']](p1['player_name'], p1['player_symbol'])
            else:
                try:
                    player1 = pickle.load(f"player-pickles/{p1['player_type']}.pkl")
                except:
                    return -1
            if p2['player_type'] in default_player_types:
                player2 = default_player_types[p2['player_type']](p2['player_name'], p2['player_symbol'])
            else:
                try:
                    player2 = pickle.load(f"player-pickles/{p2['player_type']}.pkl")
                except:
                    return -1


            self.players = [player1, player2]


            board_state = cfg['board_state']          


            self.board = Board2D(int(board_state['num_rows']), int(board_state['num_cols']), int(board_state['win_count']), player1.symbol, player2.symbol, int(board_state["current_player"]))


            if 'board' in board_state:
                self.board.state = board_state['board']


            cfg_file.close()
           
        return 0
   
    def save_config(self, fn):
        p1 = self.players[0]
        p2 = self.players[1]
        game_dict = {
            "players": [
                {
                    "player_type": p1.__class__.__name__,
                    "player_number": "0",
                    "player_name": p1.name,
                    "player_symbol": p1.symbol
                },
                {
                    "player_type": p2.__class__.__name__,
                    "player_number": "1",
                    "player_name": p2.name,
                    "player_symbol": p2.symbol
                }
            ],


            "board_state": {
                "current_player": "0",
                "num_rows": self.board.x,
                "num_cols": self.board.y,
                "win_count": self.board.n,
                "board": self.board.state
            }
        }
        with open(fn, 'w+') as f:
            f.write(json.dumps(game_dict))


    def config(self, root):
        def start_game():
            p1_name = entry_p1_name.get()
            p1_symbol = entry_p1_symbol.get()
            p1_type = p1_type_var.get()  # Correctly retrieve dropdown selection


            if len(p1_symbol) != 1:
                messagebox.showerror("Error", "Player 1 symbol must be a single character.")
                return


            # Handle bot type or player for Player 1
            if p1_type == "Load from Pickle":
                p1_bot = load_from_pickle()
                if p1_bot is None: return
                self.players[0] = p1_bot
            else:
                bot_classes = {"DumBot": DumBot, "EasyBot": EasyBot, "MediumBot": MediumBot, "HardBot": HardBot}
                if p1_type in bot_classes:
                    self.players[0] = bot_classes[p1_type](p1_name, p1_symbol)
                else:
                    self.players[0] = Player(p1_name, p1_symbol)  # Default to human player


            p2_name = entry_p2_name.get()
            p2_symbol = entry_p2_symbol.get()
            p2_type = p2_type_var.get()  # Correctly retrieve dropdown selection


            if len(p2_symbol) != 1:
                messagebox.showerror("Error", "Player 2 symbol must be a single character.")
                return


            if p1_name == p2_name:
                messagebox.showerror("Error", "Player 1 and 2 must have different names.")
                return


            if p1_symbol == p2_symbol:
                messagebox.showerror("Error", "Player 1 and 2 must have different symbols.")
                return


            # Handle bot type or player for Player 2
            if p2_type == "Load from Pickle":
                p2_bot = load_from_pickle()
                if p2_bot is None: return
                self.players[1] = p2_bot
            else:
                if p2_type in bot_classes:
                    self.players[1] = bot_classes[p2_type](p2_name, p2_symbol)
                else:
                    self.players[1] = Player(p2_name, p2_symbol)  # Default to human player


            try:
                rows = int(entry_rows.get())
                columns = int(entry_columns.get())
                win_length = int(entry_win_length.get())
            except ValueError:
                messagebox.showerror("Error", "Board dimensions and win length must be valid numbers.")
                return


            # Set up the game board
            self.board = Board2D(rows, columns, win_length, self.players[0].symbol, self.players[1].symbol, 0)
            messagebox.showinfo("Success", "Game setup completed!")
            root.quit()


        # Player 1 setup
        tk.Label(root, text="Player 1 Name").grid(row=0, column=0)
        entry_p1_name = tk.Entry(root)
        entry_p1_name.grid(row=0, column=1)


        tk.Label(root, text="Player 1 Symbol").grid(row=1, column=0)
        entry_p1_symbol = tk.Entry(root)
        entry_p1_symbol.grid(row=1, column=1)


        tk.Label(root, text="Player 1 Type").grid(row=2, column=0)
        p1_type_var = tk.StringVar(value="Human")
        p1_type_menu = tk.OptionMenu(root, p1_type_var, "Human", "DumBot", "EasyBot", "MediumBot", "HardBot", "Load from Pickle")
        p1_type_menu.grid(row=2, column=1)


        # Player 2 setup
        tk.Label(root, text="Player 2 Name").grid(row=3, column=0)
        entry_p2_name = tk.Entry(root)
        entry_p2_name.grid(row=3, column=1)


        tk.Label(root, text="Player 2 Symbol").grid(row=4, column=0)
        entry_p2_symbol = tk.Entry(root)
        entry_p2_symbol.grid(row=4, column=1)


        tk.Label(root, text="Player 2 Type").grid(row=5, column=0)
        p2_type_var = tk.StringVar(value="Human")
        p2_type_menu = tk.OptionMenu(root, p2_type_var, "Human", "DumBot", "EasyBot", "MediumBot", "HardBot", "Load from Pickle")
        p2_type_menu.grid(row=5, column=1)


        # Board setup
        tk.Label(root, text="Board Rows").grid(row=6, column=0)
        entry_rows = tk.Entry(root)
        entry_rows.grid(row=6, column=1)


        tk.Label(root, text="Board Columns").grid(row=7, column=0)
        entry_columns = tk.Entry(root)
        entry_columns.grid(row=7, column=1)


        tk.Label(root, text="Win Length").grid(row=8, column=0)
        entry_win_length = tk.Entry(root)
        entry_win_length.grid(row=8, column=1)


        # Start game button
        start_button = tk.Button(root, text="Start Game", command=start_game)
        start_button.grid(row=9, column=0, columnspan=2, pady=10)


        root.mainloop()
        return 0





