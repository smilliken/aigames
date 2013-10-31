#! /usr/bin/python

import argparse
import subprocess
import threading
from collections import defaultdict

PIPE = subprocess.PIPE


def echo_stderr(player):
    for line in iter(player.proc.stderr.readline, b''):
        print('%s debug: %s' % (player.cmd, line.strip()))


class Player(object):

    def __init__(self, cmd):
        self.cmd = cmd
        self.proc = subprocess.Popen(
            cmd, bufsize=0, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.moves = []
        self.stderr_thread = threading.Thread(target=echo_stderr, args=(self,))
        self.stderr_thread.daemon = True
        self.stderr_thread.start()

    def get_move(self):
        move = self.proc.stdout.readline()
        try:
            move = int(move.strip())
            assert 0 <= move < Game.COLUMNS
        except (ValueError, AssertionError):
            raise ValueError('invalid input from %s: %r' % (self.cmd, move))
        self.moves.append(move)
        return move

    def set_move(self, move):
        self.proc.stdin.write('%s\n' % str(move).strip())
        self.proc.stdin.flush()

    def print_moves(self):
        print('%s\t%s' % (self.cmd, ' '.join([str(move) for move in self.moves])))


class MockPlayer(object):
    def __init__(self, moves, cmd):
        self.moves = moves
        self.moved = []
        self.cmd = cmd

    def get_move(self):
        self.moved.append(self.moves.pop(0))
        return self.moved[-1]

    def set_move(self, move):
        pass

    def print_moves(self):
        print('%s\t%s' % (self.cmd, ' '.join([str(move) for move in self.moved])))


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

    def print_grid(self):
        print('-' * (Game.COLUMNS * 2 + 3))
        for row in self.grid_rows[::-1]:
            print('| %s |' % ' '.join([str(cell if cell is not None else '.') for cell in row]))
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
        for idx in xrange(0, len(series) - 3):
            if ([series[idx]] * 4 == series[idx:idx + 4] and series[idx] is not None):
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


def rungame(player0, player1):
    (current_player, next_player) = (player0, player1)
    print('%s starts' % current_player.cmd)
    current_player.set_move('go!')

    game = Game()
    while True:
        try:
            val = current_player.get_move()
        except ValueError, ex:
            print('')
            player0.print_moves()
            player1.print_moves()
            game.print_grid()
            print('%s loses: %s' % (current_player.cmd, ex.message))
            return next_player
        try:
            game.push_move(val)
        except ValueError, ex:
            print('')
            player0.print_moves()
            player1.print_moves()
            game.print_grid()
            print('%s loses: %s' % (current_player.cmd, ex.message))
            return next_player
        if game.is_won():
            print('')
            player0.print_moves()
            player1.print_moves()
            game.print_grid()
            print('%s wins!' % current_player.cmd)
            return current_player
        elif game.is_full():
            print('tie!')
        next_player.set_move(val)
        (current_player, next_player) = (next_player, current_player)


def main():
    argparser = argparse.ArgumentParser(
        description='Run two programs head-to-head in Connect Four.')
    argparser.add_argument(
        'player0', nargs='?', help='executable path of the program', default='./example-rand.py')
    argparser.add_argument(
        'player1', nargs='?', help='executable path of the program', default='./example-rand.py')
    argparser.add_argument(
        '-r', '--rounds', type=int, nargs='?', help='number of rounds to run', default=1)
    args = argparser.parse_args()
    scores = defaultdict(lambda: 0)
    for round_num in xrange(1, args.rounds + 1):
        player0 = Player(args.player0)
        player1 = Player(args.player1)
        (starter, follower) = (
            (player0, player1) if round_num % 2 == 0 else (player1, player0))
        print('\nRound %s:' % round_num)
        winner = rungame(starter, follower)
        if winner:
            scores[winner.cmd] += 1

    print('\n\nFinal Score:')
    for prog, scores in scores.iteritems():
        print('%s\t%s' % (prog.ljust(40), scores))

if __name__ == '__main__':
    main()
