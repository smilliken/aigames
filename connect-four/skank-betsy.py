#!/usr/bin/env python

# skank's brain

import sys
import copy
import argparse

import runner

FUCK_IT_MOVE = 4
DEBUG = False

def list2str(l):
    s = ""
    for ll in l:
        s += str(ll) if ll != None else " "
    return s

def nextmove(game,diagchk):
    global nnn
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
                debugit("wining move : %s" % i)
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
        debugit("no defense")
        return FUCK_IT_MOVE
    if len(okmoves) == 1:
        debugit("my only defense : %s" % okmoves[0])
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
        for symbol in [hersymbol,mysymbol]:            
            # rows
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
                            debugit("(row<<) %s will do" % (loc-1))
                            if okmove(loc-1):
                                debugit(" - and it is an okay move")    
                                return loc-1
                            else:
                                debugit(" - but not an okay move")
                            
                    try:
                        if (loc < 7 and currow[loc+l] == None):
                            try:
                                g3 = copy.deepcopy(g)
                                g3.push_move(loc)
                            except ValueError:
                                pass
                            else:
                                debugit("(row>>) %s will do" % (loc+1))
                                if okmove(loc+l):
                                    debugit(" - and it is an okay move")
                                    return loc+l
                                else:
                                    debugit(" - but not an okay move")
                    except IndexError:
                        pass

            # columns
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
                        debugit("(col) %s will do" % i)
                        if okmove(i):
                            debugit(" - and it is an okay move")
                            return i
                        else:
                            debugit(" - but not an okay move")

            # diagonals
            if diagchk:
                diagmoves = []

                if l > 2:                
                    for i in okmoves:
                        gd = copy.deepcopy(g)
                        try:
                            gd.push_move(i)
                        except ValueError:
                            continue
                        else:
                            pass

                        gdcols = gd.grid_columns
                        gdrows = gd.grid_rows

                        rdiag,ldiag = diag_at(gd,i,l)
                        srdiag = list2str(rdiag)
                        sldiag = list2str(ldiag)

                        if srdiag == str(mysymbol) + str(hersymbol)*(l-1):
                            diagmoves.append(i)
                    if len(diagmoves) > 0:
                        debugit("got a good blocking diag move : %s"%i)
                        return diagmoves[0]
            
    # nothing worked; return a safe move
    safemove = okmoves[int( (len(okmoves)) / 2)]
    try:
        ge = copy.deepcopy(g)
        ge.push_move(safemove)
    except ValueError:
        pass
    except IndexError:
        pass
    else:
        debugit('nothing worked. return a safe move : %s' % safemove)
        return safemove
    
    return FUCK_IT_MOVE

def diag_at(gg,c,n):
    ggc = copy.deepcopy(gg)
    cols = ggc.grid_columns
    rows = ggc.grid_rows

    for r,cc in enumerate(cols[c]):
        if cc == None:
            break
        
    r -= 1 #top most row of a col
    
    rdiag,ldiag = [],[]
    rc,lc = c,c
    while r >= 0:
        if lc >= 0:
            ldiag.append(rows[r][lc])
        if rc < len(rows[0]):
            rdiag.append(rows[r][rc])
        lc -= 1
        rc += 1
        r -= 1
    return [rdiag,ldiag]

def sayit(t):
    sys.stderr.write('%s\n' % t)
    sys.stderr.flush()

def debugit(t):
    if DEBUG:
        sayit("> [%s]" % t)

if __name__ == '__main__':
    # skank router
    args = sys.argv[:]
    myname = args[0].split('/')[-1]
    if "becky" in myname:
        diagchk = True
        xname = "Becky"
    else:
        diagchk = False
        xname = "Betsy"
    
    parser = argparse.ArgumentParser(description='Play Connect-4')
    parser.add_argument('--printit',required=False,action='store_true')
    parser.add_argument('--debug',required=False,action='store_true')
    parser.add_argument('--moves',required=False)
    parser.add_argument('--autopilot',required=False)
    args = vars(parser.parse_args())

    if args['autopilot']:
        autopilotn = int(args['autopilot'])
    else:
        autopilotn = 0
    
    DEBUG = args['debug']
    
    #if moves are supplied, play them
    if args['moves']:
        moves  = args['moves'].split(',')
    else:
        sayit("I'm %s, bitch!"%xname)
        moves = []
        
    game = runner.Game()
    while not sys.stdin.closed:
        if len(moves) > 0:
            line = moves.pop(0)
            sayit(line)
        elif autopilotn > 0:
            autopilotn -= 1
            line = ''
        else:
            line = sys.stdin.readline()
        if line.strip() == 'printit':
            args['printit'] = True
            continue
        try:
            l = int(line)
        except ValueError:
            pass
        else:
            game.push_move(l)
        m = nextmove(game,diagchk)
        gg = copy.deepcopy(game)
        err = False
        try:
            game.push_move(m)
        except ValueError:
            err = True
        else:
            # output move
            print m
        if err:
            for mm in range(7):
                ggz = copy.deepcopy(gg)
                try:
                    ggz.push_move(m)
                except ValueError:
                    pass
                else:
                    # output move
                    print mm
            # output move
            print FUCK_IT_MOVE

        if args['printit']:
            game.print_grid()
            
        sys.stdout.flush()
