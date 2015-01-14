#!/usr/bin/env python

import sys
import copy

import runner

def nextmove_1(game):
    move = 0
    while True:
        try:
            game.push_move(move)
        except ValueError:
            move += 1
        else:
            return move
        
def nextmove_2(game):
    # if there is a winning move, take it
    for i in range(7):
        tgame = copy.deepcopy(game)
        try:
            tgame.push_move(i)
        except ValueError:
            pass
        else:
            if tgame.is_won():
                return i

    badmoves = []
    # if the move lets the opponent win next turn, don't do it
    for i in range(7):
        for j in range(7):
            tgame = copy.deepcopy(game)
            try:
                tgame.push_move(i)
            except ValueError:
                #can't have that!
                badmoves.append(i)
                continue
            try:
                tgame.push_move(j)
            except ValueError:
                pass #they aren't going to make this move or they'll lose
            else:
                #print "checking",i,j
                #tgame.print_grid()
                if tgame.is_won():
                    badmoves.append(i)
    okmoves = list(set(range(7)) - set(badmoves))
    if len(okmoves) == 0:
        #you'll win in a move, you bastard, no matter what i do
        return 0
    else:
        #print "!", okmoves
        return okmoves[len(okmoves)/2]

# set current brain
nextmove = nextmove_2

if __name__ == '__main__':
    game = runner.Game()
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        try:
            l = int(line)
        except ValueError:
            pass
        else:
            game.push_move(l)
        m = nextmove(game)
        game.push_move(m)
        #game.print_grid()
        print m
        sys.stdout.flush()
