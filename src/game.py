from src.player import *
from src.board import *
from src.rendering import clear

import pickle
import json
import tkinter as tk


default_player_types = {
    "human": Human,
    "dumbot": DumBot,
    "easybot": EasyBot,
    "medbot": MediumBot
}
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
                break
            
            if '-' not in board.state:
                clear()
                print(board)
                print('Tie!')
                break

    def play_gui(self, root):
        player1 = self.players[0]
        player2 = self.players[1]
        players = [player1, player2]
        board = self.board

        def create_grid(board):
            grid_frame = tk.Frame(root)
            grid_frame.pack()
            buttons = []
            for i in range(board.y):
                row = []
                for j in range(board.x):
                    index = board.index_from_sq(i, j)
                    button = tk.Button(grid_frame, text=board.state[index], width=5, height=2,
                                    command=lambda row=i, col=j: button_click(row, col))
                    button.grid(row=i, column=j)
                    row.append(button)
                buttons.append(row)
            return buttons

        def disable_buttons():
            board.curr_player = -1
            for row in buttons:
                for button in row:
                    button.config(state=tk.DISABLED)

        def button_click(row, col):
            nonlocal valid_move, awaiting_human_input
            if awaiting_human_input:
                player = players[board.curr_player]
                valid_move = board.make_move(row, col) 
                if valid_move < 0:
                    print("Invalid move.")
                else:
                    awaiting_human_input = False 
                    update_grid()

        def update_grid():
            for i in range(board.y):
                for j in range(board.x):
                    index = board.index_from_sq(i, j)
                    buttons[i][j].config(text=board.state[index])

        def check_self_end():
            if board.check_win(players[board.curr_player].symbol):
                winner = players[board.curr_player]
                print(f'{winner.name} wins!')
                disable_buttons()
                self.quit_game()
                valid_move = -2
                return True
            elif board.check_win(players[1-board.curr_player].symbol):
                winner = players[1-board.curr_player]
                print(f'{winner.name} wins!')
                disable_buttons()
                self.quit_game()
                valid_move = -2
                return True
            elif board.check_draw():
                print('Draw!')
                disable_buttons()
                self.quit_game()
                valid_move = -2
                return True

        def get_move():
            nonlocal valid_move, awaiting_human_input
            if check_self_end() or self.quit: return
            player = players[board.curr_player]
            if player.type in ('human', 'player'):
                awaiting_human_input = True
            else:
                awaiting_human_input = False
                move_str = player.move(board)
                if move_str is not None:
                    try:
                        row, col = map(int, move_str.split())
                        valid_move = board.make_move(row, col) 
                        if valid_move < 0:
                            print("Invalid move.")
                    except ValueError:
                        print("Invalid move format.")

        def self_loop():
            nonlocal valid_move, awaiting_human_input

            if not self.quit:
                get_move()
                if valid_move != -1 and not awaiting_human_input:
                    update_grid()
                    valid_move = -1

                root.after(10, self_loop)

        buttons = create_grid(board)
        valid_move = -1
        awaiting_human_input = False
        
        self_loop()
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

            self.board.state = board_state['board']

            cfg_file.close()
            
        return 0

    def config(self):
        clear()
        p1_type = str(input('Player 1 (Human: 0. DumBot: 1, EasyBot: 2, MediumBot: 3): '))
        clear()

        p1_name = str(input('Player 1 Name: '))
        clear()
        
        p1_symbol = str(input('Player 1 Symbol: '))
        while(len(p1_symbol) != 1):
            clear()
            print('Player 1 must be a single character')
            p1_symbol = str(input('Player 1 Symbol: '))
        clear()

        if p1_type == '1':
            self.players[0] = DumBot(p1_name, p1_symbol)
        if p1_type == '2':
            self.players[0] = EasyBot(p1_name, p1_symbol)
        if p1_type == '3':
            self.players[0] = MediumBot(p1_name, p1_symbol)
        else:
            self.players[0] = Player(p1_name, p1_symbol)

        p2_type = str(input('Player 2 (Human: 0, DumBot: 1, EasyBot: 2, MediumBot: 3): '))
        clear()

        p2_name = str(input('Player 2 Name: '))
        while p1_name == p2_name:
            clear()
            print('Player 1 and 2 must have different names')
            p2_name = str(input('Player 2 Name: '))
        clear()

        p2_symbol = str(input('Player 2 Symbol: '))
        while p1_symbol == p2_symbol or len(p2_symbol) != 1:
            clear()
            if p1_symbol == p2_symbol:
                print('Player 1 and 2 must have different characters')
            if len(p2_symbol) != 1:
                print('Player 2 must be a single character')
            p2_symbol = str(input('Player 2 Symbol: '))
        clear()

        if p2_type == '1':
            self.players[1] = DumBot(p2_name, p2_symbol)
        if p2_type == '2':
            self.players[1] = EasyBot(p2_name, p2_symbol)
        if p2_type == '3':
            self.players[1] = MediumBot(p2_name, p2_symbol)
        else:
            self.players[1] = Player(p2_name, p2_symbol)


        x = str(input('Board Rows: '))
        while not x.isnumeric():
            clear()
            print('Board Rows must be a number')
            x = str(input('Board Rows: '))
        clear()

        y = str(input('Board Columns: '))
        while not y.isnumeric():
            clear()
            print('Board Columns must be a number')
            y = str(input('Board Columns: '))
        clear()

        n = str(input('Win Length: '))
        while not n.isnumeric():
            clear()
            print('Win Length must be a number')
            n = str(input('Win Length: '))
        clear()


        self.board = Board2D(int(x), int(y), int(n), self.players[0].symbol, self.players[1].symbol, 0)

        clear()

        return 0