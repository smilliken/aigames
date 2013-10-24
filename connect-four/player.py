#! /usr/bin/python

import sys
from copy import deepcopy as copy

import runner
Game = runner.Game

range1 = [3,2,4,1,5,0,6]

def alphabeta(game, depth, a, b, player_is_zero, heuristic):
    # if game.is_won():
    #     return playeror game.is_full()
    # game.print_grid()
    if game.is_won():
        return 100000 if player_is_zero else -100000
    if depth == 0:
        return heuristic((game.grid_columns, game.grid_rows, game.diags))
    if player_is_zero:
        for i in range1:
            try:
                result = alphabeta(copy(game).push_move(i), depth - 1, a, b, False, heuristic)
            except:
                # print "invalid"
                result = -100000
            a = max([a, result])
            if b <= a:
                # print result
                # print a, b
                break
        return a
    else:
        for i in range1:
            try:
                result = alphabeta(copy(game).push_move(i), depth - 1, a, b, True, heuristic)
            except:
                # print "invalid"
                result = 100000
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
        for i in range1:
            try:
                result = alphabeta(copy(game).push_move(i), depth - 1, a, b, False, heuristic)
            except:
                # print "invalid"
                result = -100000
            if result > a:
                a = result
                bestmove = i
            # a = max([a, move_val[i]])
            if b <= a:
                # print result
                # print a, b
                break
        # for i in range1:
        #     if move_val[i] == a:
        return bestmove
    else:
        for i in range1:
            try:
                result = alphabeta(copy(game).push_move(i), depth - 1, a, b, True, heuristic)
            except:
                # print "invalid"
                result = 100000
            if result < b:
                b = result
                bestmove = i
            # b = min([b, result])
            if b <= a:
                # print result
                # print a, b
                break
        # for i in range1:
        #     if move_val[i] == b:
        return bestmove

def score(t):
    for tt in t:
        s1,s2 = 1,1
        for z in tt:
            if z == 0:
                s1 = s1 * 10
                s2 = 1
            elif z == 1:
                s2 = s2 * 10
                s1 = 1
    return s1/s2

def score2(t):
    for tt in t:
        sc = 0
        s1,s2 = 1,1
        for i,z in enumerate(tt):
            if z == 0:
                s1 = s1 * 10
                if 10**(6-i) < s1:
                    s1 = 0
                s2 = 1
            elif z == 1:
                s2 = s2 * 10
                if 10**(6-i) < s2:
                    s2 = 0
                s1 = 1
        s = s1/s2
        sc += s
    return sc

def score3(t):
    for tt in t:
        for ttt in tt:
            sc = 0
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
            s = s1/s2
            sc += s
            print(s, s1, s2)
    print sc
    return sc

def score4(z):
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
            s = s1/s2
            sc += s
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
        sys.stdout.flush()


def printi(str_):
    pass
    # sys.stderr.write("%s\n" % str_)

if __name__ == '__main__':
    # while not sys.stdin.closed:
    #     line = sys.stdin.readline()
    #     print(1)
    #     sys.stdout.flush()
    player(3, score4)
