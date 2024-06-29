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
        return str_to_s(inst[4:])
    else:
        err(f"unknown instruction label in ({inst})")

def to_s(ascii_ch: str) -> str:
    index = S_ASCII.index(ascii_ch)
    return chr(33 + index)

def str_to_s(text: str) -> str:
    return 'S' + ''.join([
        to_s(ascii_ch)
        for ascii_ch in text
    ])

def s_to_str(s: str) -> str:
    return ''.join([
        S_ASCII[ord(ch)-33]
        for ch in s
    ])

def base94(body: str) -> int:
    i = 0
    for ch in body:
        i *= 94
        i += ord(ch) - ord('!')
    return i

def int_to_str(i: int) -> str:
    result = ''
    while i:
        d = i % 94
        i -= d
        i //= 94
        result += S_ASCII[d]
    return result[::-1]

def str_to_int(s: str) -> int:
    i = 0
    for ch in s:
        i *= 94
        index = S_ASCII.index(ch)
        i += index
    return i

def evaluate(icfp: str) -> str:
    tokens = tokenize(icfp)
    result, _ = eval_tokens(tokens[0], tokens[1:])
    return result

def eval_tokens(token: str, rest: list[str]) -> tuple[str, list[str]]:
    indicator = token[0]
    body = token[1:]
    match indicator:
        case 'T': return 'true', rest
        case 'F': return 'false', rest
        case 'I': return str(base94(body)), rest
        case 'S': return s_to_str(body), rest
        case 'U':
            x, rest = eval_tokens(rest[0], rest[1:])
            match body:
                case '-':
                    return str(-int(x)), rest
                case '!':
                    return icfp_bool(not str_to_bool(x)), rest
                case '#':
                    return str(str_to_int(x)), rest
                case '$':
                    return int_to_str(int(x)), rest
                case _:
                    err(f'bad U body "{body}" in "{token}"')
                    return '', rest
        case 'B':
            x, rest = eval_tokens(rest[0], rest[1:])
            y, rest = eval_tokens(rest[0], rest[1:])
            match body:
                case '+':
                    return str(int(x) + int(y)), rest
                case '-':
                    return str(int(x) - int(y)), rest
                case '*':
                    return str(int(x) * int(y)), rest
                case '/':
                    int_x = int(x)
                    int_y = int(y)
                    is_neg = (int_x < 0 and int_y > 0) or (int_x > 0 and int_y < 0)
                    int_div = abs(int_x) // abs(int_y)
                    #print(f"{int_x} {int_y} {int_div} {is_neg}")
                    return str(-int_div) if is_neg else str(int_div), rest
                case '%':
                    int_x = int(x)
                    int_y = int(y)
                    is_neg = (int_x < 0 and int_y > 0) or (int_x > 0 and int_y < 0)
                    int_mod = abs(int_x) % abs(int_y)
                    #print(f"{int_x} {int_y} {int_mod} {is_neg}")
                    return str(-int_mod) if is_neg else str(int_mod), rest
                case '<':
                    return icfp_bool(int(x) < int(y)), rest
                case '>':
                    return icfp_bool(int(x) > int(y)), rest
                case '=':
                    return icfp_bool(int(x) == int(y)), rest
                case '|':
                    return icfp_bool(str_to_bool(x) or str_to_bool(y)), rest
                case '&':
                    return icfp_bool(str_to_bool(x) and str_to_bool(y)), rest
                case '.':
                    return x + y, rest
                case 'T':
                    return y[:int(x)], rest
                case 'D':
                    return y[int(x):], rest
                case '$':
                    err('lambda not done ($)')
                    return '', rest
                case _:
                    err(f'bad B body "{body}" in "{token}"')
                    return '', rest
        case '?':
            b, rest = eval_tokens(rest[0], rest[1:])
            if str_to_bool(b):
                return eval_tokens(rest[0], rest[1:])
            else:
                return eval_tokens(rest[1], rest[2:])
        case 'L':
            err(f'lambda not done (L)')
        case _:
            err(f'bad indicator "{indicator}" in "{token}"')
            return '', rest


def str_to_bool(s: str) -> bool:
    return s == 'true'

def icfp_bool(tf: bool) -> str:
    return 'true' if tf else 'false'


def tokenize(icfp: str) -> list[str]:
    return icfp.split(sep=' ')


def get(what: str) -> str:
    """
    Invoke a cult service.
    """
    program = ['STR get '+what]
    icfp = assemble(program)
    r = post(icfp)
    return evaluate(r.text)

def send(text: str) -> str:
    """
    Send `text` to the cult.
    Note that:
    $python3 cmds/send.py get index
    is the same as get (above).
    """
    program = [f'STR {text}']
    r = post(assemble(program))
    return evaluate(r.text)


def err(what: str, code: int = 1) -> None:
    print(f"error: {what}")
    exit(code)


def post(message: str):
    r = requests.post(
            CULT_URL,
            headers={'Authorization': TEAM_AUTHORIZATION},
            data=message)
    if r.status_code != 200:
        err(f'bad http post status {r.status_code}')
    return r
