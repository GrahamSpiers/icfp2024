# [scoreboard] service

from icfp.icfp import assemble, evaluate, post

program = ['STR get scoreboard']

icfp = assemble(program)
r = post(icfp)
print(evaluate(r.text))