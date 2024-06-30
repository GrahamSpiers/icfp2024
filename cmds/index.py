# index.py
# Show my [index]

from icfp.icfp import assemble, post
from icfp.hypermi import hyper_evaluate

program = ['STR get index']

icfp = assemble(program)
r = post(icfp)
print(hyper_evaluate(r.text))

