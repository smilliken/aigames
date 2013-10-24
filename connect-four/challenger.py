#!/usr/bin/env python
'''
I am always X. opfor is always O.
'''
import sys
import copy


def score(board):
    # Really simple heuristic.
    # Counts the number of x's in the longest column
    def score(col):
        return sum([1 if row == 'x' else 0 for row in col])
    return max(map(score, board.columns))


def minimax(board, depth, shouldMaximize):
    pass


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

    def playerat(self, row, column):
        # Returns what is at (x, y)
        # the origin is at the bottom left
        if not (0 <= row < 6) or not (0 <= column < 7) or not self.isValidMove(column):
            return 'z'
        return self.columns[column][row]

    def isValidMove(self, col):
        return any([row == ' ' for row in self.columns[col]])

    @staticmethod
    def isOnBoard(row, column):
        return 0 <= row < self.ROWS and 0 <= column < self.COLUMNS

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


INITIAL_DEPTH = 3
def findBestNextMoveForX(board):
    bestMoveSoFar = 0
    bestScoreSoFar = -10000000
    for i in range(7):
        if not board.isValidMove(i):
            continue
        nextScore = miniMaxScore(board.move(i, 'x'), INITIAL_DEPTH, 'x')
        if nextScore > bestScoreSoFar:
          bestMoveSoFar = i
          bestScoreSoFar = nextScore
    return bestMoveSoFar

def miniMaxScore(board, depth, playerToMaximize):
  if depth == 0:
    return getScore(board)
  
  if playerToMaximize == 'x':
    bestScore = -10000000
    for i in range(7):
      if (board.isValidMove(i)):
        nextScore = miniMaxScore(board.move(i, 'o'), depth - 1, 'o')
        bestScore = max(nextScore, bestScore)
    return bestScore
  else: #then player is 'o'
    bestScore = 10000000
    for i in range(7):
      if (board.isValidMove(i)):
        nextScore = miniMaxScore(board.move(i, 'x'), depth - 1, 'x')
        bestScore = min(nextScore, bestScore) 
    return bestScore

def getScore(board):
  xPlayerScore = 0
  yPlayerScore = 0
  winningPlayer = playerHasWon(board)
  if winningPlayer == 'x':
    return 1000000
  elif winningPlayer == 'o':
    return -1000000
  
  for col in range(7):
    for row in range(6):
      playerAtPosition = board.playerat(row, col)
      if playerAtPosition == 'x':
        xPlayerScore += evaluateCoordinate(board, col, row)
      elif playerAtPosition == 'o':
        yPlayerScore += evaluateCoordinate(board, col,row)
  return xPlayerScore - yPlayerScore


def evaluateCoordinate(board, col,row):
  totalScore = 0
  player = board.playerat(row, col)

  # tie break
  if col == 0:
    pass
  elif row == 5:
    pass
  elif col == 6:
    pass
  elif col == 1:
    totalScore +=1
  elif col == 5:
    totalScore +=1
  elif row == 4:
    totalScore +=1
  else:
    totalScore +=2 
  return totalScore


def playerHasWon(board):
  for col in range(7):
    for row in range(6):
      #col win
      curr = board.playerat(row, col)
      if curr == ' ':
        pass
      elif (curr == board.playerat(row+1,col)
        and curr == board.playerat(row+2,col)
        and curr == board.playerat(row+3,col)):
        return curr
      elif (curr == board.playerat(row,col+1)
        and curr == board.playerat(row,col+2)
        and curr == board.playerat(row,col+3)):
        return curr
      elif (curr == board.playerat(row+1,col+1)
        and curr == board.playerat(row+2,col+2)
        and curr == board.playerat(row+3,col+3)):
        return curr
      elif (curr == board.playerat(row-1,col-1)
        and curr == board.playerat(row-2,col-2)
        and curr == board.playerat(row-3,col-3)):
        return curr


if __name__ == '__main__':
    board = Board()

    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line == 'go!\n':
            print('3')
            board = board.move(3, 'x')
        else:
            board = board.move(int(line), 'o')
            move = findBestNextMoveForX(board)
            print(move)
            board = board.move(move, 'x')
        sys.stdout.flush()
