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

from sys import argv, maxsize
from icfp.icfp import get, send


type Pt = tuple[int, int] # row, col

MOVES: dict[str, Pt] = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

BAD = 'NO SOLUTION'

class VisitMap:
    def __init__(self, h: int, w: int) -> None:
        self.visits = [
            [0 for _ in w]
            for _ in h
        ]
    def visit(self, pt: Pt) -> None:
        self.visits[pt[0]][pt[1]] += 1
    def row(self, row: int) -> list[int]:
        return self.visits[row]
    def max_visits(self) -> int:
        return max([
            max(self.row(r))
            for r in range(len(self.visits))
        ])


class Puzzle:
    def __init__(self, s_puzzle: str) -> None:
        self.rows: list[str] = s_puzzle.split()
        self.h = len(self.rows)
        self.w = len(self.rows[0])
        self.pt_start = self.start()
        self.must_eat = self.pills()
        self.good = self.must_eat | {self.pt_start}
    def solve(self) -> str:
        # list[(dir, path_so_far, last_pt, visited)]
        to_try = [
            (dir, '', self.pt_start, set())
            for dir in MOVES.keys()
        ]
        max_depth = 0
        while to_try:
            if len(to_try) > max_depth:
                max_depth = len(to_try)
                print(f'depth {max_depth}')
            next_dir, so_far, pt, visited = to_try.pop(0)
            delta = MOVES[next_dir]
            next_pt = (pt[0] + delta[0], pt[1] + delta[1])
            if not self.is_good(next_pt):
                continue
            next_so_far = so_far + next_dir
            next_visited = visited.copy()
            if next_pt != self.pt_start:
                next_visited |= {next_pt}
                if next_visited == self.must_eat:
                    return next_so_far
            to_try += [
                (dir, next_so_far, next_pt, next_visited)
                for dir in MOVES.keys()
            ]
        return BAD
    def solve2(self) -> str:
        path = ''
        pt = self.pt_start
        eaten = set()
        while eaten != self.must_eat:
            pt_next = self.nearest_uneaten(pt, eaten)
            steps, eaten_on_way = self.walk(pt, pt_next)
            path += steps
            eaten |= eaten_on_way
            pt = pt_next
        return path
    def walk(self, pt0: Pt, pt1: Pt) -> tuple[str, set[Pt]]:
        # pt dir path steps eaten_on_way
        to_try = [
            (pt0, dir, '', set(), set())
            for dir in MOVES.keys()
        ]
        while to_try:
            pt, dir, path, steps, eaten = to_try.pop(0)
            drc = MOVES[dir]
            next_pt = (pt[0]+drc[0], pt[1]+drc[1])
            if next_pt in steps or not self.is_good(next_pt):
                continue
            next_path = path + dir
            next_steps = steps | {pt}
            next_eaten = eaten.copy()
            if next_pt in self.must_eat:
                next_eaten.add(next_pt)
            if pt1 == next_pt:
                return next_path, next_eaten
            to_try += [
                (next_pt, dir, next_path, next_steps, next_eaten)
                for dir in MOVES.keys()
            ]
        return BAD, set()
    def nearest_uneaten(self, pt: Pt, eaten: set[Pt]) -> Pt:
        pt_best = (-1, -1)
        dsq_best = maxsize
        for pt1 in self.must_eat:
            if not pt1 in eaten:
                dr = pt1[0] - pt[0]
                dc = pt1[1] - pt[1]
                dsq = dr*dr + dc*dc
                if dsq < dsq_best:
                    pt_best = pt1
                    dsq_best = dsq
        return pt_best
    def start(self) -> Pt:
        for row in range(self.h):
            for col in range(self.w):
                if self.at((row, col)) == 'L':
                    return (row, col)
    def pills(self) -> set[Pt]:
        return self.all('.')
    def all(self, ch: str) -> set[Pt]:
        return {
            (row, col)
            for row in range(self.h)
            for col in range(self.w)
            if self.at((row, col)) == ch
        }
    def is_good(self, pt: Pt) -> bool:
        return pt in self.good
    def at(self, pt: Pt) -> str:
        return self.rows[pt[0]][pt[1]]

for number in argv[1:]:
    s_puzzle = get(f'lambdaman{number}')
    print(s_puzzle)
    puzzle = Puzzle(s_puzzle)
    path = puzzle.solve2()
    print(path)
    if not BAD in path:
        print(send(f"solve lambdaman{number} {path}"))
