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
        move = find_winning_moves(board, self.symbol)[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])

class EasyBot(Player):
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
        
        win_chances = create_win_chances(board, self.symbol)
        move = win_chances[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = block_win_chances(board)
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = random.sample(board.legal_moves(), 1)[0]
        return ' '.join([str(i) for i in board.sq_from_index(move)])
    
    
class HardBot(Player):
    def __init__(self, name: str, symbol: chr, max_depth=5):
        super().__init__(name, symbol)
        self.type = 'bot'
        self.max_depth = max_depth

    def move(self, board: Board2D):

        move = find_winning_moves(board, self.symbol)[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        move = find_winning_moves(board, board.players[1-board.curr_player])[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        win_chances = create_win_chances(board, self.symbol)
        move = win_chances[0]
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])

        move = block_win_chances(board)
        if move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(move)])
        
        if board.curr_player == 0:
            best_score = [-10] + [0]*board.n
            best_move = -1
            for move in board.legal_moves():
                test_board = board.__copy__()
                i, j = board.sq_from_index(move)
                test_board.make_move(i, j)
                score = minimax(test_board, self.max_depth, [-10]+board.n*[0], [10]+board.n*[0])
                if compare_score(score, best_score) > 0:
                    best_move = move
                    best_score = score

        if board.curr_player == 1:
            best_score = [10] + [0]*board.n
            best_move = -1
            for move in board.legal_moves():
                test_board = board.__copy__()
                i, j = board.sq_from_index(move)
                test_board.make_move(i, j)
                score = minimax(test_board, self.max_depth, [-10]+board.n*[0], [10]+board.n*[0])
                if compare_score(score, best_score) < 0:
                    best_move = move
                    best_score = score
        
        if best_move >= 0:
            return ' '.join([str(i) for i in board.sq_from_index(best_move)])

        return ' '.join([str(i) for i in board.sq_from_index(random.sample(board.legal_moves(), 1)[0])])
                



    

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
    max_count = 2
    max_move = []
    for move in board.legal_moves():
        test_board = board.__copy__()
        i, j = board.sq_from_index(move)
        test_board.set_square(player, i, j)
        count = len(find_winning_moves(test_board, player))

        if count == max_count:
            max_move.append(move)

        if count > max_count:
            max_count = count
            max_move = [move]

    if len(max_move) == 0:
        return [-1]

    return max_move
    
def block_win_chances(board: Board2D):
    player = board.players[board.curr_player]
    opponent = board.players[1-board.curr_player]
    if len(create_win_chances(board, opponent)) > 0:
        for move in board.legal_moves():
            test_board = board.__copy__()
            i, j = board.sq_from_index(move)
            test_board.set_square(player, i, j)
            chances = len(create_win_chances(test_board, opponent))
            if chances < 1:
                return move
    return -1

def evaluate(board):
    score = [0]*(board.n+1)
    #check rows
    for i in range(board.x):
        row = list(board.state[board.x*i:board.x*i+board.y])
        score_part = get_score(row, board)
        score = [score[i] + score_part[i] for i in range(board.n+1)]

    #check cols
    for j in range(board.y):
        col = [board.state[j + i*board.y] for i in range(board.x)]
        score_part = get_score(col, board)
        score = [score[i] + score_part[i] for i in range(board.n+1)]
        
    #check diag lr
    for j in range(-board.x + board.n, board.y):
        diag = [board.state[(j + i) + board.y*i] if ((j+i) >= 0 and (j+i) < board.y) else '-' for i in range(board.x)]
        score_part = get_score(diag, board)
        score = [score[i] + score_part[i] for i in range(board.n+1)]
    

    #check diag rl
    for j in range(0, board.y - board.n):
        diag = [board.state[(j - i) + board.y*i] if ((j-i) >= 0 and (j-i) < board.y) else '-' for i in range(board.x)]
        score_part = get_score(diag, board)
        score = [score[i] + score_part[i] for i in range(board.n+1)]

    return score

def get_score(ax, board):
    n = board.n
    p1 = board.p1
    p2 = board.p2
    start = 0
    score = [0]*(n+1)


    while start+n <= len(ax):
        line = ax[start:start+n]
        if len(line) < n:
            continue
        if p2 not in line:
            s = sum([1 if c == p1 else 0 for c in line])
            for i in range(s+1):
                score[i] += 1

        if p1 not in line:
            s = sum([1 if c == p2 else 0 for c in line])
            for i in range(s+1):
                score[i] -= 1
        start += 1
    return [score[i] for i in range(n, -1, -1)]

def compare_score(score_1, score_2):
    for i, j in zip(score_1, score_2):
        if i > j: return 1
        if j > i: return -1
    return 0

def max_score(score_1, score_2):
    for i, j in zip(score_1, score_2):
        if i > j: return score_1
        if j > i: return score_2
    return score_1

def min_score(score_1, score_2):
    for i, j in zip(score_1, score_2):
        if i > j: return score_2
        if j > i: return score_1
    return score_1

def minimax(board, depth, alpha, beta):
    evaluation = evaluate(board)
    if depth == 0:
        return evaluation
    if evaluation[0] != 0:
        return evaluation
    if board.check_draw():
        return [0] * (board.n+1)
    
    if board.curr_player == 0:
        score = [-10] + [0]*board.n
        for move in board.legal_moves():
            test_board = board.__copy__()
            i, j = board.sq_from_index(move)
            test_board.make_move(i, j)
            score = max_score(score, minimax(test_board, depth-1, alpha, beta))
            if compare_score(score, beta) >= 0:
                break
            alpha = max_score(alpha, score)
        return score

    if board.curr_player == 1:
        score = [10] + [0]*board.n
        for move in board.legal_moves():
            test_board = board.__copy__()
            i, j = board.sq_from_index(move)
            test_board.make_move(i, j)
            score = min_score(score, minimax(test_board, depth-1, alpha, beta))
            if compare_score(score, alpha) <= 0:
                break
            beta = min_score(beta, score)
        return score


