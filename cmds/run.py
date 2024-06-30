# interpret_file.py
# Evaluate some ICFP from a file and show the result.

from sys import argv
#from icfp.icfp import evaluate
from icfp.hypermi import hyper_evaluate

for filename in argv[1:]:
    with open(filename, 'r') as f_in:
        s = f_in.read()
        print(hyper_evaluate(s))
