error_codes = {
    -1: "Move must be a number",
    -2: "Move Outside of Board",
    -3: "Space already taken"
}

class Board2D:
    def __init__(self, x: int=3, y: int=3, n: int=3, p1: str='X', p2: str='O', curr_player: int=0):
        self.state = '-'*x*y
        self.x = x
        self.y = y
        self.n = n
        self.p1 = p1
        self.p2 = p2
        self.players = [p1, p2]
        self.moveseq = []
        self.curr_player = curr_player

    def __copy__(self):
        board_str = self.save_board()
        board_params = board_str.split(' ')
        x, y, n, p1, p2, curr_player, board = board_params
        copy = Board2D(int(x), int(y), int(n), p1, p2, int(curr_player))
        copy.state = board
        return copy

    def __str__(self):
        string_representation = '  '
        for j in range(self.y):
            string_representation += str(j) + ' '
        string_representation += '\n'
        for i in range(self.x):
            string_representation += str(i) + ' '
            for j in range(self.y):
                string_representation += self.state[self.y*i + j] + ' '
            string_representation += '\n'
        return string_representation
    
    def get_arr(self):
        arr_dict = {'-': 0, self.p1: 1, self.p2: 2}
        return [[arr_dict[self.state[self.index_from_sq(i, j)]] for j in range(self.y)] for i in range(self.x)]

    def get_board_state(self):
        return self.state

    def save_board(self):
        board_str = f'{self.x} {self.y} {self.n} {self.p1} {self.p2} {self.curr_player} {self.state}'
        return board_str

    def set_board(self, board_str: str):
        board_params = board_str.split(' ')
        x, y, n, p1, p2, curr_player, board = board_params
        self = Board2D(int(x), int(y), int(n), p1, p2, int(curr_player))
        self.state = board

    def set_square(self, player, i, j):
        board_list = list(self.state)
        board_list[self.y*i + j] = player
        self.state = ''.join(board_list)

    def index_from_sq(self, i, j):
        if i not in list(range(0, self.x)) or j not in list(range(0, self.y)):
            return -1
        else: return self.y*i + j

    def sq_from_index(self, i):
        return i//self.y, i%self.y

    def legal_moves(self):
        return [pos for pos, char in enumerate(list(self.state)) if char == '-']

    def make_move(self, i: int, j: int):
        if not str(i).isnumeric() or not str(j).isnumeric():
            return -1

        i, j = int(i), int(j)
        if i >= self.x or j >= self.y:
            return -2
        if self.state[self.y*i + j] != '-':
            return -3
        else:
            self.set_square(self.players[self.curr_player], i, j)
            self.curr_player = 1 - self.curr_player
            self.moveseq.append([self.players[self.curr_player], i, j])
            return 0

    def check_win(self, player):
        #check_rows
        for i in range(self.x):
            if player*self.n in self.state[self.x*i:self.x*i+self.y]:
                return True

        #check_cols
        for j in range(self.y):
            if player*self.n in "".join([self.state[j + i*self.y] for i in range(self.x)]):
                return True
            
        #check diag lr
        for j in range(-self.x+1, self.y):
            diag = "".join([self.state[(j + i) + self.y*i] if ((j+i) >= 0 and (j+i) < self.y) else '-' for i in range(self.x)])
            if player*self.n in diag:
                return True
        

        #check diag rl
        for j in range(0, self.y + self.y - 1):
            diag = "".join([self.state[(j - i) + self.y*i] if ((j-i) >= 0 and (j-i) < self.y) else '-' for i in range(self.x)])
            if player*self.n in diag:
                return True
        
        return False

    def check_draw(self):
        if '-' not in self.state:
            return True

    def config():
        p1 = str(input('Player 1: '))
        while(len(p1) != 1):
            print('Player 1 must be a single character')
            p1 = str(input('Player 1: '))
        p2 = str(input('Player 2: '))
        while p1 == p2 or len(p2) != 1:
            if p1 == p2:
                print('Player 1 and 2 must have different characters')
                p2 = str(input('Player 2: '))
            if len(p2) != 1:
                print('Player 2 must be a single character')
                p2 = str(input('Player 2: '))
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

        return Board2D(int(x), int(y), int(n), p1, p2)