#!/usr/bin/env python
'''
I am always X. opfor is always O.
'''
import sys
import copy
import functools


class InvalidMove(Exception):
    pass


class Board(object):
    ROWS = 6
    COLUMNS = 7

    def __init__(self, state=None):
        # from left to right
        if state:
            self.columns = state
        else:
            def makecolumn():
                return [' '] * self.ROWS
            self.columns = [makecolumn() for _ in range(self.COLUMNS)]

    def __str__(self):
        rep = 'Board: \n'
        for row in reversed(self.rows):
            rep += ' | '.join(list(row)) 
            rep += '\n'
        return rep

    def count(self):
        count = 0
        for column in self.columns:
            for row in column:
                count += 0 if row == ' ' else 1
        return count

    def column(self, col):
        # from bottom to top
        return self.columns[col]

    def row(self, row):
        return [col[row] for col in self.columns]

    @property
    def rows(self):
        return [self.row(i) for i in range(self.ROWS)]

    @property
    def diags(self):
        indicies = [
            # Lefties
            [(0, 3), (1, 2), (2, 1), (3, 0)],
            [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)],
            [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)],
            [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)],
            [(2, 5), (3, 4), (4, 3), (5, 2), (6, 1)],
            [(3, 5), (4, 4), (5, 3), (6, 2)],
            # Righties
            [(0, 2), (1, 3), (2, 4), (3, 5)],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
            [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)],
            [(2, 0), (3, 1), (4, 2), (5, 3), (6, 4)],
            [(3, 0), (4, 1), (5, 2), (6, 3)],
        ]
        def mapper(coords):
            return [self.columns[col][row] for col, row in coords]
        return [mapper(coords) for coords in indicies]

    def playerat(self, row, column):
        # Returns what is at (x, y)
        # the origin is at the bottom left
        return self.columns[column][row]

    def valid_moves(self):
        def valid(move):
            return any([row == ' ' for row in self.columns[move]])
        return [i for i in range(self.COLUMNS) if valid(i)]

    def move(self, col, player):
        if player not in ('x', 'o'):
            raise Exception('BAD PLAYER %s' % player)
        if not (0 <= col < 7):
            raise Exception('BAD MOVE %s' % col)

        newcolumns = copy.deepcopy(self.columns)
        newboard = Board(newcolumns)

        for row in range(self.ROWS):
            currplayer = self.playerat(row, col)
            if currplayer == ' ':
                newboard.columns[col][row] = player
                return newboard

        raise InvalidMove('column %s is already full!' % col)

    def winner(self):
        def four_connected(row):
            curr = None
            count = 0
            for char in row:
                if char == ' ':
                    curr = None
                    continue
                if char == curr:
                    count += 1
                    if count == 3:
                        return char
                elif char != curr:
                    curr = char
                    count = 0
            return None

        for col in self.columns:
            if four_connected(col):
                return four_connected(col)

        for row in self.rows:
            if four_connected(row):
                return four_connected(row)

        for diag in self.diags:
            if four_connected(diag):
                return four_connected(diag)

        return None


def score(board):
    if board.winner() == 'x':
        return 1
    if board.winner() == 'o':
        return -1
    return 0


def minimaxscore(board, xnext=True, ply=0):
    if ply == 0 or board.winner() != None:
        return score(board)
    if xnext:
        bestscore = -1
        for move in board.valid_moves():
            newscore = minimaxscore(board.move(move, 'x'), xnext=False, ply=ply-1)
            bestscore = max(bestscore, newscore)
        return bestscore
    else:
        bestscore = 1
        for move in board.valid_moves():
            newscore = minimaxscore(board.move(move, 'o'), xnext=True, ply=ply-1)
            bestscore = min(bestscore, newscore)
        return bestscore


def best_move(board, maximizex):
    if maximizex:
        bestscore = -1
        bestmove = None
        for move in board.valid_moves():
            newscore = minimaxscore(board.move(move, 'x'), xnext=False, ply=4)
            if newscore > bestscore:
                bestmove = move
                bestscore = newscore
        if bestmove is None:
            return board.valid_moves()[0]
        return bestmove
    else:
        bestscore = 1
        bestmove = None
        for move in board.valid_moves():
            newscore = minimaxscore(board.move(move, 'o'), xnext=True, ply=4)
            if newscore < bestscore:
                bestmove = move
                bestscore = newscore
        if bestmove is None:
            return board.valid_moves()[0]
        return bestmove


def apply_moves(board, moves, xFirst):
    char = 'x' if xFirst else 'o'
    for move in moves:
        board = board.move(move, char)
        char = 'x' if char == 'o' else 'o'
    return board


blank = Board()
white_to_win = apply_moves(blank, [3, 0, 2, 0, 0, 0, 0, 0, 2, 1, 6, 1, 4], False)

def sim():
    board = Board()
    print white_to_win
    print 'best x move:', best_move(white_to_win, True)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        sim()
    board = Board()

    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line == 'go!\n':
            print('3')
            board = board.move(3, 'x')
        else:
            board = board.move(int(line), 'o')
            move = best_move(board, True)
            print(move)
            board = board.move(move, 'x')
        sys.stdout.flush()
