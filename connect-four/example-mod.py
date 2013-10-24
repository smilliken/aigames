#! /usr/bin/python

import sys

if __name__ == '__main__':
    move = 0
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        print(move)
        sys.stdout.flush()
        move = (move + 1) % 7
