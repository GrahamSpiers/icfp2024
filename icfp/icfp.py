# icfp common stuff package

import requests
from icfp.error import err
from icfp.tfis import str_to_tok_s
from icfp.hypermi import hyper_evaluate


CULT_URL = 'https://boundvariable.space/communicate'

TEAM_AUTHORIZATION = 'Bearer 921df178-ab9d-43a9-ad36-fc844c4647b6'

# Assembly
# Turned out to be not needed.

def assemble(program: list[str]) -> str:
    """
    Assemble a program (a list of instructions).  Possible instructions are:
        STR s   Where s is a string.  Becomes ICFP SX where X is ICFP indicator 'S' text.
    """
    return ' '.join([
        assemble_instruction(inst)
        for inst in program
    ])

def assemble_instruction(inst: str) -> str:
    if inst.startswith('STR '):
        return str_to_tok_s(inst[4:])
    else:
        err(f"unknown instruction label in ({inst})")

# Communications

def get(what: str) -> str:
    """
    Invoke a cult service.
    """
    program = ['STR get '+what]
    icfp = assemble(program)
    r = post(icfp)
    return hyper_evaluate(r.text)

def send(text: str) -> str:
    """
    Send `text` to the cult.
    Note that:
    $python3 cmds/send.py get index
    is the same as get (above).
    """
    program = [f'STR {text}']
    r = post(assemble(program))
    return hyper_evaluate(r.text)

def show(text: str) -> str:
    """
    Send text to the cult.
    Just return the result (no evaluate!).
    """
    program = [f'STR {text}']
    r = post(assemble(program))
    return r.text

def post(message: str):
    r = requests.post(
            CULT_URL,
            headers={'Authorization': TEAM_AUTHORIZATION},
            data=message)
    if r.status_code != 200:
        err(f'bad http post status {r.status_code}')
    return r


