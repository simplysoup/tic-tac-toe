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