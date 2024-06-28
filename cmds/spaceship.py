# spaceship.py
# Solve the given spaceship puzzle.
#
# spaceship1
# 1 -1
# 1 -3
# 2 -5
# 2 -8
# 3 -10

from sys import argv, maxsize
from typing import Optional
from icfp.icfp import get, send


type Pt = tuple[int, int] # row, col

MOVES: dict[str, Pt] = {
    '1': (-1, -1),
    '2': (0, -1),
    '3': (1, -1),
    '4': (-1, 0),
    '5': (0, 0),
    '6': (1, 0),
    '7': (-1, 1),
    '8': (0, 1),
    '9': (1, 1),
}
print(MOVES)

REVERSE_MOVES: dict[Pt, str] = {
    pt: dir
    for dir, pt in MOVES.items()
}
print(REVERSE_MOVES)

def solve(s_puzzle: str) -> str:
    to_visit = parse_to_visit(s_puzzle)
    moves = ''
    v: Pt = (0, 0)
    pt: Pt = (0, 0)
    while to_visit:
        pt_next = pt_nearest(pt, to_visit)
        print(f"{pt} -> {pt_next}")
        v, pt, d_moves = move(v, pt, pt_next)
        moves += d_moves
        to_visit.remove(pt_next)
    return moves

def move(v: Pt, pt: Pt, pt_to: Pt) -> tuple[Pt, Pt, str]:
    moves = ''
    while pt != pt_to:
        delta: Pt = (sign(pt_to[0] - pt[0]), sign(pt_to[1] - pt[1]))
        v, move = change_v(v, delta)
        moves += move
        pt = (pt[0] + v[0], pt[1] + v[1])
        print(f"\t{pt}")
    return v, pt, moves

def change_v(v: Pt, delta: Pt) -> tuple[Pt, str]:
    dv = (sign(delta[0]-v[0]), sign(delta[1]-v[1]))
    move = REVERSE_MOVES[dv]
    return (v[0] + dv[0], v[1] + dv[1]), move

def sign(v: int) -> int:
    if v > 0:
        return 1
    elif v < 0:
        return -1
    else:
        return 0

def pt_nearest(pt: Pt, pts: set[Pt]) -> Pt:
    closest: Optional[Pt] = None
    closest_dsq = maxsize
    for test_pt in pts:
        dx = test_pt[0] - pt[0]
        dy = test_pt[1] - pt[1]
        dsq = dx*dx + dy*dy
        if dsq < closest_dsq:
            closest = test_pt
            closest_dsq = dsq
    return closest

def parse_to_visit(s_puzzle: str) -> set[Pt]:
    return {
        line_to_pt(line)
        for line in s_puzzle.split('\n')
        if line
    }

def line_to_pt(line: str) -> Pt:
    s_x, s_y = line.split()
    return (int(s_x), int(s_y))


def follow(moves: str) -> None:
    """
    Debug function that follows some moves.
    """
    pt: Pt = (0, 0)
    v: Pt = (0, 0)
    for move in moves:
        dv = MOVES[move]
        v = (v[0] + dv[0], v[1] + dv[1])
        pt = (pt[0] + v[0], pt[1] + v[1])
        print(f"{move} {v} {pt}")


for number in argv[1:]:
    s_puzzle = get(f'spaceship{number}')
    print(s_puzzle)
    moves = solve(s_puzzle)
    #follow(moves)
    print(moves)
    print(send(f"solve spaceship{number} {moves}"))
