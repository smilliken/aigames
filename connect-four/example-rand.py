#! /usr/bin/python

import random
import sys

if __name__ == '__main__':
    while not sys.stdin.closed:
        line = sys.stdin.readline()
        move = random.randint(0, 6)
        print(move)
        sys.stdout.flush()
