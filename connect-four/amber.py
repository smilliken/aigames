#!/usr/bin/env python

import sys
import copy

import runner

def list2str(l):
    s = ""
    for ll in l:
        s += str(ll) if ll != None else " "
    return s

def nextmove_3(game):

    # --- old code begin
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
                if tgame.is_won():
                    badmoves.append(i)

    badmoves = list(set(badmoves))
    okmoves = list(set(range(7)) - set(badmoves))
    if len(okmoves) == 0:
        #you'll win in a move, you bastard, no matter what i do
        return 4
    if len(okmoves) == 1:
        return okmoves[0]
    # --- old code end

    def okmove(move1):
        return (move1 in okmoves)
    
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
                        if okmove(i): return i
                    
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
                            if okmove(loc-1): return loc-1
                    try:
                        if (loc < 7 and currow[loc+l] == None):
                            try:
                                g3 = copy.deepcopy(g)
                                g3.push_move(loc)
                            except ValueError:
                                pass
                            else:
                                if okmove(loc+l): return loc+l
                    except IndexError:
                        pass

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
    try:
        ge = copy.deepcopy(g)
        ge.push_move(okmoves[0])
    except ValueError:
        pass
    else:
        okmoves[0]
    return 4

if __name__ == '__main__':
    args = sys.argv[:]
    myname = args[0].split('/')[-1]

    #if moves are supplied, play them
    if len(args) > 1:
        moves  = list(args[1])
    else:
        moves = []
        
    nextmove = nextmove_3
        
    game = runner.Game()
    while not sys.stdin.closed:
        if len(moves) > 0:
            line = moves.pop(0)
            print line
        else:
            line = sys.stdin.readline()
        try:
            l = int(line)
        except ValueError:
            pass
        else:
            game.push_move(l)
        m = nextmove(game)
        gg = copy.deepcopy(game)
        err = False
        try:
            game.push_move(m)
        except ValueError:
            err = True
        else:
            print m
        if err:
            for mm in range(7):
                ggz = copy.deepcopy(gg)
                try:
                    ggz.push_move(m)
                except ValueError:
                    pass
                else:
                    print mm
        #game.print_grid()
        sys.stdout.flush()
