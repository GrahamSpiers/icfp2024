# 3d test
#
# $ python3 cmds/test3d.py 3d/test.3d 5 6
#
# Would run the 3d program test.3d with A=5 and B=6.

from sys import argv
from icfp.icfp import assemble, eval, post

filename = argv[1]
A = argv[2]
B = None
if len(argv) > 3:
    B = argv[3]

if B:
    print(f'{filename} A={A} B={B}')
else:
    print(f'{filename} A={A}')

def read_3d_prog(filename: str) -> str:
    with open(filename, 'r') as f_in:
        return f_in.read()

prog_3d = read_3d_prog(filename)
#print(prog_3d)

program = [f'STR test 3d {A} {B}\n{prog_3d}']
#print(program)
a = assemble(program)
#print(a)
r = post(a)
print(r.text)
print(eval(r.text))
