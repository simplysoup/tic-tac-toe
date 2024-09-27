from src.player import Player, DumBot
from src.board import Board2D

class Game:
    def __init__(self, x: int=3, y: int=3, n: int=3, players: list=[Player('Human', 'X'), DumBot('Random', 'O')]):
        self.board = Board2D(x, y, n, players[0].symbol, players[1].symbol, 0)
        self.players = players
        self.curr_player = 0
    def play(self):
        player1 = self.players[0]
        player2 = self.players[1]
        players = [player1, player2]
        board = self.board
        while True:
            player = players[board.curr_player]
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
                print(board)
                print(f'{player.name} Wins!')
                break
            
            if '-' not in board.board:
                print(board)
                print('Tie!')
                break

    def config(self):

        p1_type = str(input('Player 1 (Bot: 0, Human: 1): '))
        while p1_type != '0' and p1_type != '1':
            print('Invalid input')
            p1_type = str(input('Player 1 (Bot: 0, Human: 1): '))

        p1_name = str(input('Player 1 Name: '))
        
        p1_symbol = str(input('Player 1 Symbol: '))
        while(len(p1_symbol) != 1):
            print('Player 1 must be a single character')
            p1_symbol = str(input('Player 1 Symbol: '))

        if p1_type == '0':
            self.players[0] = DumBot(p1_name, p1_symbol)
        else:
            self.players[0] = Player(p1_name, p1_symbol)

        p2_type = str(input('Player 2 (Bot: 0, Human: 1): '))
        while p2_type != '0' and p2_type != '1':
            print('Invalid input')

        p2_name = str(input('Player 2 Name: '))
        while p1_name == p2_name:
            print('Player 1 and 2 must have different names')
            p2_name = str(input('Player 2 Name: '))

        p2_symbol = str(input('Player 2 Symbol: '))
        while p1_symbol == p2_symbol or len(p2_symbol) != 1:
            if p1_symbol == p2_symbol:
                print('Player 1 and 2 must have different characters')
                p2 = str(input('Player 2 Symbol: '))
            if len(p2_symbol) != 1:
                print('Player 2 must be a single character')
                p2 = str(input('Player 2 Symbol: '))


        if p2_type == '0':
            self.players[1] = DumBot(p2_name, p2_symbol)
        else:
            self.players[1] = Player(p2_name, p2_symbol)



        x = str(input('Board Rows: '))
        while not x.isnumeric():
            print('Board Rows must be a number')
            x = str(input('Board Rows: '))
        y = str(input('Board Columns: '))
        while not y.isnumeric():
            print('Board Columns must be a number')
            y = str(input('Board Columns: '))
        n = str(input('Win Length: '))
        while not n.isnumeric():
            print('Win Length must be a number')
            n = str(input('Win Length: '))
        
        self.board = Board2D(int(x), int(y), int(n), self.players[0].symbol, self.players[1].symbol, 0)
               
if __name__ == "main.py":
	g = Game()
	g.config()
	g.play()