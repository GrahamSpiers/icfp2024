# send.py
# Send some text to the cult.

from sys import argv
from icfp.icfp import send

print(send(' '.join(argv[1:])))