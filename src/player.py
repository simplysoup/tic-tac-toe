import random
from src.board import Board2D

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
        #print(test_board)
        valid_move = -1
        while valid_move < 0:
            move = [str(random.randint(0, test_board.x-1)), str(random.randint(0, test_board.y-1))]
            valid_move = test_board.make_move(move[0], move[1])
        return ' '.join(move)

class EasyBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)


    