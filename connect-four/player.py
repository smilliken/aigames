#! /usr/bin/python

import sys
from copy import deepcopy as copy

range1 = [3,2,4,1,5,0,6]


class Game(object):

    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.moves = []
        self.grid_columns = [[None for _ in xrange(Game.ROWS)] for _ in xrange(Game.COLUMNS)]
        self.grid_rows = [[None for _ in xrange(Game.COLUMNS)] for _ in xrange(Game.ROWS)]

    def push_move(self, move):
        col_idx = int(move)
        # insert move into grid_columns
        for row_idx, cell in enumerate(self.grid_columns[col_idx]):
            if cell is None:
                self.grid_columns[col_idx][row_idx] = len(self.moves) % 2
                break
        else:
            raise ValueError('invalid move! column %s is full.' % col_idx)
        # insert move into grid_rows
        self.grid_rows[row_idx][col_idx] = len(self.moves) % 2
        self.moves.append(col_idx)
        return self

    @property
    def valid_moves(self):
        return [i for i in range1 if self.grid_rows[5][i] is None]

    def print_grid(self):
        print('-' * (Game.COLUMNS * 2 + 3))
        for row in self.grid_rows[::-1]:
            print('| %s |' % ' '.join([str(cell if cell is not None else ' ') for cell in row]))
        print('-' * (Game.COLUMNS * 2 + 3))

    def is_won(self):
        return (self.any_columns_won() or self.any_rows_won() or
            self.any_diags_won())

    def is_full(self):
        return len(self.moves) == Game.ROWS * Game.COLUMNS

    def any_columns_won(self):
        return any(self.check_series(column) for column in self.grid_columns)

    def any_rows_won(self):
        return any(self.check_series(row) for row in self.grid_rows)

    def any_diags_won(self):
        return any(self.check_series(diag) for diag in self.diags)

    def check_series(self, series):
        if len(series) < 4:
            return False
        for idx in xrange(0, len(series) - 4):
            if ([series[idx]] * 4 == series[idx:idx + 4] and
                    all((x is not None for x in series[idx:idx + 4]))):
                return True
        return False

    @property
    def diags(self):
        def get_diags(right=True):
            return [
                [self.grid_rows[r + delta][c + (delta if right else -delta)]
                    for delta in xrange(min(Game.ROWS - r, (Game.COLUMNS - c if right else c)))]
                for r in xrange(Game.ROWS)
                for c in xrange(Game.COLUMNS)]
        return get_diags(right=True) + get_diags(right=False)


def alphabeta(game, depth, a, b, player_is_zero, heuristic):
    # if game.is_won():
    #     return playeror game.is_full()
    # game.print_grid()
    if game.is_won():
        return 100000 if player_is_zero else -100000
    if depth == 0:
        return heuristic(game)
    if player_is_zero:
        for i in game.valid_moves:
            result = alphabeta(copy(game).push_move(i), depth - 1, a, b, False, heuristic)
            a = max([a, result])
            if b <= a:
                # print result
                # print a, b
                break
        return a
    else:
        for i in game.valid_moves:
            result = alphabeta(copy(game).push_move(i), depth - 1, a, b, True, heuristic)
            b = min([b, result])
            if b <= a:
                # print result
                # print a, b
                break
        return b

def call_alphabeta(game, depth, a, b, player_is_zero, heuristic):
    move_val = range1
    bestmove = 1
    if player_is_zero:
        for i in game.valid_moves:
            result = alphabeta(copy(game).push_move(i), depth - 1, a, b, False, heuristic)
            if result > a:
                a = result
                bestmove = i
                print a, b, result, bestmove
            # a = max([a, move_val[i]])
            if b <= a:
                # print result
                # print a, b
                break
        # for i in range1:
        #     if move_val[i] == a:
        return bestmove
    else:
        for i in game.valid_moves:
            result = alphabeta(copy(game).push_move(i), depth - 1, a, b, True, heuristic)
            if result < b:
                b = result
                bestmove = i
                print a,b,result,bestmove
            # b = min([b, result])
            if b <= a:
                # print result
                # print a, b
                break
        # for i in range1:
        #     if move_val[i] == b:
        return bestmove

def itersafe(n):
    return n if n else None

def potential(board):
    # board.print_grid()
    base = 10
    score = 0
    _ = board.grid_rows + board.grid_columns + board.diags
    # print _
    # print board.grid_rows
    for line in _:
        if len(line) < 4:
            continue
        zeros = [1 if cell == 0 else 0 for cell in line]
        ones = [1 if cell == 1 else 0 for cell in line]

        zeros = map(lambda *args: sum(args), *[zeros[i:itersafe(-4 + i)] for i in range(4)])
        ones = map(lambda *args: sum(args), *[ones[i:itersafe(-4 + i)] for i in range(4)])

        for i in range(len(zeros)):
            # print zeros[i], ones[i]
            score += pow(base,zeros[i]) if not ones[i] else 0
            score -= pow(base,ones[i]) if not zeros[i] else 0

    return score


def score5(z):
    sc = 0
    for t in z:
        for tt in t:
            s1,s2 = 1,1
            if len(tt) < 4:
                continue
            for i,z in enumerate(tt):
                if z == 0:
                    s1 = s1 * 10
                    if s1 >= 1000:
                        return 999999
                    if 10**(6-i) < s1:
                        s1 = 0
                    s2 = 1
                elif z == 1:
                    s2 = s2 * 10
                    if s2 >= 1000:
                        return -999999
                    if 10**(6-i) < s2:
                        s2 = 0
                    s1 = 1
            # s = s1/s2
            sc += s1 + s2
    return sc


def player(depth, heuristic):
    game = Game()
    player_is_zero = False
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line == 'go!':
            player_is_zero = True
        else:
            game.push_move(line)
        move = call_alphabeta(game, depth, -10000000, 10000000, player_is_zero, heuristic)
        # printi(move)
        # assert(int(move) >= 0)
        # print(1)
        # print(score3(game))
        print(move)
        game.push_move(move)
        game.print_grid()
        sys.stdout.flush()


def printi(str_):
    pass
    # sys.stderr.write("%s\n" % str_)

if __name__ == '__main__':
    # while not sys.stdin.closed:
    #     line = sys.stdin.readline()
    #     print(1)
    #     sys.stdout.flush()
    player(3, potential)
