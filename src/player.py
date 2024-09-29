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
        move = find_winning_moves(board, self.symbol)[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])

class MediumBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'bot'

    def move(self, board: Board2D):
        move = find_winning_moves(board, self.symbol)[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = find_winning_moves(board, board.players[1-board.curr_player])[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = random.sample(board.legal_moves(), 1)[0]
        return ' '.join([str(i) for i in board.sq_from_index(move)])
    
class HardBot(Player):
    def __init__(self, name: str, symbol: chr):
        super().__init__(name, symbol)
        self.type = 'bot'

    def move(self, board: Board2D):
        move = find_winning_moves(board, self.symbol)[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = find_winning_moves(board, board.players[1-board.curr_player])[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = create_win_chances(board, self.symbol)
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = create_win_chances(board, board.players[1-board.curr_player])
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = random.sample(board.legal_moves(), 1)[0]
        return ' '.join([str(i) for i in board.sq_from_index(move)])
    

def find_winning_moves(board: Board2D, player: str):
    wins = []
    for move in board.legal_moves():
        test_board = board.__copy__()
        i, j = board.sq_from_index(move)
        test_board.set_square(player, i, j)
        winning = test_board.check_win(player)

        if winning:
            wins.append(move)
    if len(wins) == 0:
        wins.append(-1)
    return wins

def create_win_chances(board: Board2D, player: str):
    max_count = 1
    max_move = -1
    for move in board.legal_moves():
        test_board = board.__copy__()
        i, j = board.sq_from_index(move)
        test_board.set_square(player, i, j)
        count = len(find_winning_moves(test_board, player))
        if count > max_count:
            max_count = count
            max_move = move
    return max_move
    