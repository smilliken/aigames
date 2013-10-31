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
                    
            #for i,currow in enumerate(rows):
                
            
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
