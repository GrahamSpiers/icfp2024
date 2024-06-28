# lambdaman.py
# Solve the given lambdaman puzzle.
#
# lambdaman1
#
# ##.#...
# ...L..##
# .#######
#
# a solution: LLLDURRRUDRRURR

from sys import argv
from icfp.icfp import get, send


type Pt = tuple[int, int] # row, col

MOVES = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

class Puzzle:
    def __init__(self, s_puzzle: str) -> None:
        self.rows: list[str] = s_puzzle.split()
        self.h = len(self.rows)
        self.w = len(self.rows[0])
        self.pt_start = self.start()
        self.must_visit = self.empty()
        self.walls = self.walls()
    def solve(self) -> str:
        # list[(dir, path_so_far, last_pt, visited)]
        to_try = [
            (dir, '', self.pt_start, {self.pt_start})
            for dir in MOVES.keys()
        ]
        while to_try:
            next_dir, so_far, last_pt, visited = to_try.pop(0)
            if visited == self.must_visit:
                return so_far
            delta = MOVES[next_dir]
            next_pt = (last_pt[0] + delta[0], last_pt[1] + delta[1])
            if not self.is_good(next_pt):
                continue
            next_so_far = so_far + next_dir
            next_visited = visited | {next_pt}
            to_try += [
                (dir, next_so_far, next_pt, next_visited)
                for dir in MOVES.keys()
            ]
        return 'NO SOLUTION'
    def start(self) -> Pt:
        for row in range(self.h):
            for col in range(self.w):
                if self.at((row, col)) == 'L':
                    return (row, col)
    def empty(self) -> set[Pt]:
        return self.all('.') | {self.pt_start}
    def walls(self) -> set[Pt]:
        return self.all('#')
    def all(self, ch: str) -> set[Pt]:
        return {
            (row, col)
            for row in range(self.h)
            for col in range(self.w)
            if self.at((row, col)) == ch
        }
    def is_good(self, pt: Pt) -> bool:
        return pt in self.must_visit
    def at(self, pt: Pt) -> str:
        return self.rows[pt[0]][pt[1]]




for number in argv[1:]:
    s_puzzle = get(f'lambdaman{number}')
    print(s_puzzle)
    puzzle = Puzzle(s_puzzle)
    path = puzzle.solve()
    print(path)
    print(send(f"solve lambdaman{number} {path}"))
