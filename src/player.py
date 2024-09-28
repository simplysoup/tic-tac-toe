import random
from src.board import *
import multiprocessing

class Player:
    def __init__(self, name: str, symbol: chr):
        self.name = name
        self.symbol = symbol
        self.type = 'player'
    def move(self, board: Board2D):
        return str(input())

class Human(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'human'
    def move(self, board: Board2D):
        return str(input())

class DumBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'bot'

    def move(self, board: Board2D):
        test_board = board.__copy__()
        i, j = board.sq_from_index(random.sample(board.legal_moves(), 1)[0])
        return ' '.join([str(j), str(i)])

class EasyBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'bot'

    def move(self, board: Board2D):
        move = find_winning_move(board, self.symbol)
        if move > 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])

class MediumBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'bot'
        with open('log.txt', 'w+') as f:
            f.write('')
            f.close()

    def log(self, board, move, note):
        with open('log.txt', 'a+') as f:
            f.write(' '.join([str(i) for i in board.sq_from_index(move)]) + note + "\n")
            f.close()

    def move(self, board: Board2D):
        move = find_winning_move(board, self.symbol)
        if move >= 0:
            self.log(board, move, 'winning')
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = find_winning_move(board, board.players[1-board.curr_player])
        if move >= 0:
            self.log(board, move, 'saving')
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = random.sample(board.legal_moves(), 1)[0]
        self.log(board, move, "random")
        return ' '.join([str(i) for i in board.sq_from_index(move)])
    
    

        
import time

def find_winning_move(board: Board2D, player: str):
    for move in board.legal_moves():
        test_board = board.__copy__()
        i, j = board.sq_from_index(move)
        test_board.set_square(player, i, j)
        winning = test_board.check_win(player)

        if winning:
            return move
    return -1
