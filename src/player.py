import random
from src.board import *
import multiprocessing

class Player:
    def __init__(self, name: str, symbol: chr):
        self.name = name
        self.symbol = symbol
    def move(self, board: Board2D):
        return str(input())

class DumBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)

    def move(self, board: Board2D):
        test_board = board.__copy__()
        i, j = board.sq_from_index(random.sample(board.legal_moves(), 1)[0])
        return ' '.join([str(i), str(j)])

class EasyBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)

    def move(self, board: Board2D):
        move = find_winning_move(board, self.symbol)
        if move > 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])

class MediumBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)

    def move(self, board: Board2D):
        move = find_winning_move(board, self.symbol)
        print(move)
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = find_winning_move(board, board.players[1-board.curr_player])
        print(move)
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])

        


def find_winning_move(board: Board2D, player: str):
    for move in board.legal_moves():
        test_board = board.__copy__()
        i, j = board.sq_from_index(move)
        test_board.set_square(player, i, j)
        winning = test_board.check_win(player)

        if winning:
            return move
    return -1
