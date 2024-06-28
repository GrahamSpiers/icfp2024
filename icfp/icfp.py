# icfp common stuff package

import requests
from sys import exit


CULT_URL = 'https://boundvariable.space/communicate'

TEAM_AUTHORIZATION = 'Bearer 921df178-ab9d-43a9-ad36-fc844c4647b6'

S_ASCII = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n'''


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
        return 'S' + ''.join([
            to_s(ascii_ch)
            for ascii_ch in inst[4:]
        ])
    else:
        err(f"unknown instruction label in ({inst})")

def to_s(ascii_ch: str) -> str:
    index = S_ASCII.index(ascii_ch)
    return chr(33 + index)


def eval(icfp: str) -> str:
    #print(f"icfp:({icfp})")
    return '\n'.join([
        eval_token(token)
        for token in tokenize(icfp)
    ])

def eval_token(token: str) -> str:
    #print(f"token({token})")
    match token[0]:
        case 'S':
            return ''.join([
                S_ASCII[ord(ch)-33]
                for ch in token[1:]
            ])
        case _:
            err(f'unknown indicator ({token[0]}) in {token}')
            return ""

def tokenize(icfp: str) -> list[str]:
    return icfp.split(sep=' ')


def get(what: str) -> str:
    """
    Invoke a cult service.
    """
    program = ['STR get '+what]
    icfp = assemble(program)
    r = post(icfp)
    return eval(r.text)

def send(text: str) -> str:
    """
    Send `text` to the cult.
    """
    program = [f'STR {text}']
    r = post(assemble(program))
    return eval(r.text)


def err(what: str, code: int = 1) -> None:
    print(f"error: {what}")
    exit(code)


def post(message: str) -> None:
    return requests.post(
            CULT_URL,
            headers={'Authorization': TEAM_AUTHORIZATION},
            data=message)
