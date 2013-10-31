#!/usr/bin/env python

# skank's brain

import sys
import copy

import runner

def list2str(l):
    s = ""
    for ll in l:
        s += str(ll) if ll != None else " "
    return s

def nextmove_3(game):

    # --- old begin
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
        return 4
    # --- old end
    
    tgame = copy.deepcopy(game)
    mysymbol = len(tgame.moves)%2
    hersymbol = abs(mysymbol - 1)

    g = copy.deepcopy(tgame)
    cols = g.grid_columns
    rows = g.grid_rows
    
    for l in [3,2,1]:
        for symbol in [mysymbol,hersymbol]:
            for i,curcol in enumerate(cols):
                xc = []
                for cc in curcol:
                    if cc == None:
                        break
                    else:
                        xc.append(cc)
                if len(xc)<l:
                    continue
                ctop = xc[len(xc)-l:]
                if list2str(ctop) == str(symbol)*l:
                    try:
                        g1 = copy.deepcopy(g)
                        g1.push_move(i)
                    except ValueError:
                        pass
                    else:
                        return i
                    
            for i,currow in enumerate(rows):
                s = list2str(currow)
                loc = s.find(str(symbol)*l)                
                if loc > -1:
                    if (loc > 0 and currow[loc-1] == None):
                        try:
                            g2 = copy.deepcopy(g)
                            g2.push_move(loc)
                        except ValueError:
                            pass
                        else:
                            return loc-1
                    if (loc < 7 and currow[loc+l] == None):
                        try:
                            g3 = copy.deepcopy(g)
                            g3.push_move(loc)
                        except ValueError:
                            pass
                        else:
                            return loc+l

    #diagonals
    for symbol in [mysymbol,hersymbol]:
        for l in range(1,7):
            gd = copy.deepcopy(g)
            c = cols[l]
            #get top of col as n
            for n,xx in enumerate(c):
                if xx == None:
                    break
            

    
    # nothing worked; return a safe move
    for i in range(7):
        try:
            ge = copy.deepcopy(g)
            ge.push_move(i)
        except ValueError:
            pass
        else:
            return i
    return 4

if __name__ == '__main__':
    # skank router
    args = sys.argv[:]
    myname = args[0].split('/')[-1]
    nextmove = nextmove_3
        
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
        game.print_grid()
        print m
        sys.stdout.flush()
