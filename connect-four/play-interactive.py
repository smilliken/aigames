#!/usr/bin/env python

# Author : aigames@kirubakaran.com

import sys
import runner

def next_move():
    return 1

def main():
    game = runner.Game()
    
    def endit(msg):
        print game.print_grid()
        print msg
        sys.exit()
        return

    while not sys.stdin.closed:
        line = sys.stdin.readline()
        if line.strip() == "exit":
            endit("Bye.")
        try:
            l = int(line)
        except ValueError:
            print "Okay I'll go ..."
        else:
            try:
                game.push_move(l)
            except ValueError:
                endit("You made an invalid move and lost. AI won.")
            else:
                if game.is_won():
                    endit("You won")
                elif game.is_full():
                    endit("Tie")
            game.print_grid()
            
        move = next_move()
        print("me: %s"%(move,))
        try:
            game.push_move(move)
        except ValueError:
            endit("AI made an invalid move and lost. You won.")
        else:
            if game.is_won():
                endit("AI won")
            elif game.is_full():
                endit("Tie")
            else:
                game.print_grid()
        sys.stdout.flush()
        
if __name__ == '__main__':
    main()
