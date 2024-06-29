# index.py
# Show my [index]

from icfp.icfp import assemble, evaluate, post

program = ['STR get index']

icfp = assemble(program)
r = post(icfp)
print(evaluate(r.text))

