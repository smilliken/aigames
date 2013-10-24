#! /usr/bin/python

import copy
import random
import sys


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
        # insert move into grid_rows
        self.grid_rows[row_idx][col_idx] = len(self.moves) % 2
        self.moves.append(col_idx)

    def print_grid(self):
        print('-' * (Game.COLUMNS * 2 + 3))
        for row in self.grid_rows[::-1]:
            print('| %s |' % ' '.join([str(cell if cell is not None else ' ') for cell in row]))
        print('-' * (Game.COLUMNS * 2 + 3))

    def column_height(self, col_idx):
        return len([x for x in self.grid_columns[col_idx] if x is not None])

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
        '''Return whether there are 4 in a row.'''
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

def pick_random(choices):
    if choices:
        return random.choice(choices)
    return

def get_next_move(game):
    # we're starting, choose middle
    if not game.moves:
        return Game.COLUMNS / 2
    # any possible 4-in-a-rows this turn?
    for out_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        game2.push_move(out_move)
        if game2.is_won():
            return out_move

    move_blacklist = [x for x in xrange(game.COLUMNS) if game.column_height(x) >= game.ROWS]
    # don't enable any 4-in-a-rows in the next opponent move
    for our_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        game2.push_move(our_move)
        for their_move in xrange(game.COLUMNS):
            game3 = copy.deepcopy(game2)
            game3.push_move(their_move)
            if game3.is_won():
                move_blacklist.append(our_move)

    # choose based on our parity
    move = pick_random([x for x in xrange(Game.COLUMNS)
        if x % 2 == len(game.moves) % 2
        and x not in move_blacklist])
    if move is not None:
        return move
    # no other ideas, choose random
    move = pick_random([x for x in xrange(Game.COLUMNS) if x not in move_blacklist])
    if move is not None:
        return move
    return 3

def log(msg):
    sys.stderr.write('%s\n' % msg)
    sys.stderr.flush()

def main():
    game = Game()
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        try:
            move = int(line.strip())
            game.push_move(move)
        except ValueError:
            pass
        our_move = get_next_move(game)
        print(our_move)
        sys.stdout.flush()
        game.push_move(our_move)

def test(test_moves=[6, 6, 4, 0, 0, 0]):
    game = Game()
    for move in test_moves:
        game.push_move(move)
        our_move = get_next_move(game)
        print(our_move)
        sys.stdout.flush()
        game.push_move(our_move)


if __name__ == '__main__':
    # test()
    main()
