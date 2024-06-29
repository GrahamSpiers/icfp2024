# 3d.py
# No clue...

from sys import argv, maxsize
from icfp.icfp import get, send


for number in argv[1:]:
    s_puzzle = get(f'3d{number}')
    print(s_puzzle)
    #moves = solve(s_puzzle)
    #follow(moves)
    #print(moves)
    #print(send(f"solve spaceship{number} {moves}"))
