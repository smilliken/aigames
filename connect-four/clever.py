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

    def is_won(self, runlen=4):
        return (self.any_columns_won(runlen) or self.any_rows_won(runlen) or
            self.any_diags_won(runlen))

    def is_full(self):
        return len(self.moves) == Game.ROWS * Game.COLUMNS

    def any_columns_won(self, runlen=None):
        return any(self.check_series(column, runlen) for column in self.grid_columns)

    def any_rows_won(self, runlen=None):
        return any(self.check_series(row, runlen) for row in self.grid_rows)

    def any_diags_won(self, runlen=None):
        return any(self.check_series(diag, runlen) for diag in self.diags)

    def check_series(self, series, runlen):
        '''Return whether there are `runlen` in a row.'''
        if len(series) < runlen:
            return False
        for idx in xrange(0, len(series) - runlen + 1):
            if ([series[idx]] * runlen == series[idx:idx + runlen] and
                    all((x is not None for x in series[idx:idx + runlen]))):
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
        return random.choice(list(choices))

def pick_min(choices):
    if choices:
        return min(choices)

def get_next_move(game):
    '''
    A very hacky rules-based approach. Only looks ahead one move and is in major need of
    refactoring.
    '''
    # any possible 4-in-a-rows this turn?
    for out_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        game2.push_move(out_move)
        if game2.is_won():
            trash_talk([
                'ohhh yea!', 'another win for clever', 'yeah yeah yeah', 'checkmate!', 'too easy'])
            return out_move

    legal_moves = set([
        x for x in xrange(game.COLUMNS) if game.column_height(x) < game.ROWS])
    really_bad_moves = set([])
    kinda_bad_moves = set([])
    kinda_good_moves = set([])

    # don't enable any 4-in-a-rows in the next opponent move
    for our_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        game2.push_move(our_move)
        for their_move in xrange(game.COLUMNS):
            game3 = copy.deepcopy(game2)
            game3.push_move(their_move)
            if game3.is_won():
                really_bad_moves.add(our_move)

    # prefer no 3-in-a-rows in the next opponent move
    for our_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        game2.push_move(our_move)
        for their_move in xrange(game.COLUMNS):
            game3 = copy.deepcopy(game2)
            if game3.is_won(runlen=3):
                continue
            game3.push_move(their_move)
            if game3.is_won(runlen=3):
                kinda_bad_moves.add(our_move)

    # prefer that we get 3-in-a-rows
    for our_move in xrange(game.COLUMNS):
        game2 = copy.deepcopy(game)
        if game2.is_won(runlen=3):
            continue
        game2.push_move(our_move)
        if game2.is_won(runlen=3):
            kinda_good_moves.add(our_move)

    kinda_bad_moves.update(really_bad_moves)

    # try kinda good moves...
    move = pick_random(kinda_good_moves.difference(kinda_bad_moves))
    if move is not None:
        log('kind good move', move)
        return move
    # try legal moves that aren't bad...
    move = pick_random(legal_moves.difference(kinda_bad_moves))
    if move is not None:
        log('legal not bad move', move)
        return move
    # try any legal move that isn't really bad...
    move = pick_random(legal_moves.difference(really_bad_moves))
    if move is not None:
        trash_talk(['hmm..', 'bah', 'pfft'])
        log('legal not really bad', move)
        return move
    # ok, try any legal move
    trash_talk(['fuuuuuu.....', 'touche', 'ughh'])
    return pick_random(legal_moves)

def log(msg, move=None):
    return
    sys.stderr.write('%s %s\n' % (msg, move or ''))
    sys.stderr.flush()

def trash_talk(quotes):
    sys.stderr.write('%s\n' % pick_random(quotes))
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
