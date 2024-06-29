# icfp common stuff package

import requests
from sys import exit


CULT_URL = 'https://boundvariable.space/communicate'

TEAM_AUTHORIZATION = 'Bearer 921df178-ab9d-43a9-ad36-fc844c4647b6'

S_ASCII = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n'''

I_BASE = 94
ZERO_INDEX = 33

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
    result = evaluate_icfp(tokens)
    return result


def extract_icfp(tokens: list[str]) -> tuple[list[str], list[str]]:
    """
    Extract the tokens for the ICFP from 'tokens'.
    """
    token = tokens[0]
    rest = tokens[1:]
    indicator = token[0]
    #body = token[1:]
    match indicator:
        case 'T': return [token], rest
        case 'F': return [token], rest
        case 'I': return [token], rest
        case 'S': return [token], rest
        case 'U':
            x, rest = extract_icfp(rest)
            return [token] + x, rest
        case 'B':
            x, rest = extract_icfp(rest)
            y, rest = extract_icfp(rest)
            return [token] + x + y, rest
        case '?':
            cond, rest = extract_icfp(rest)
            yes, rest = extract_icfp(rest)
            no, rest = extract_icfp(rest)
            return [token] + cond + yes + no, rest
        case 'L':
            func, rest = extract_icfp(rest)
            return [token] + func, rest
        case 'v':
            return [token], rest
        case _:
            err(f'bad indicator "{indicator}" in "{token}"')
            return [], rest

def evaluate_icfp(icfp: list[str], vars: dict[str, list[str]] = {}, later: list[list[str]] = []) -> str:
    """
    Process a tokens into a string.
    """
    print(f"evaluate_icfp {icfp}")
    token, rest = icfp[0], icfp[1:]
    indicator = token[0]
    body = token[1:]
    match indicator:
        case 'T': return 'true'
        case 'F': return 'false'
        case 'I': return str(base94(body))
        case 'S': return s_to_str(body)
        case 'U':
            x_icfp, rest = extract_icfp(rest)
            print(x_icfp)
            x = evaluate_icfp(x_icfp, vars)
            print(x)
            match body:
                case '-':
                    return str(-int(x))
                case '!':
                    return icfp_bool(not str_to_bool(x))
                case '#':
                    return str(str_to_int(x))
                case '$':
                    return int_to_str(int(x))
                case _:
                    err(f'bad U body "{body}" in "{token}"')
                    return ''
        case 'B':
            x_icfp, rest = extract_icfp(rest)
            print(x_icfp)
            y_icfp, rest = extract_icfp(rest)
            print(y_icfp)
            if body == '$':
                # apply
                # y is rest
                later.append(y_icfp)
                return evaluate_icfp(x_icfp, vars, later)
            x = evaluate_icfp(x_icfp, vars, later)
            print(x)
            y = evaluate_icfp(y_icfp, vars, later)
            print(y)
            #print(f'x:"{x}" y:"{y}"')
            match body:
                case '+':
                    return str(int(x) + int(y))
                case '-':
                    return str(int(x) - int(y))
                case '*':
                    return str(int(x) * int(y))
                case '/':
                    int_x = int(x)
                    int_y = int(y)
                    is_neg = (int_x < 0 and int_y > 0) or (int_x > 0 and int_y < 0)
                    int_div = abs(int_x) // abs(int_y)
                    #print(f"{int_x} {int_y} {int_div} {is_neg}")
                    return str(-int_div) if is_neg else str(int_div)
                case '%':
                    int_x = int(x)
                    int_y = int(y)
                    is_neg = (int_x < 0 and int_y > 0) or (int_x > 0 and int_y < 0)
                    int_mod = abs(int_x) % abs(int_y)
                    #print(f"{int_x} {int_y} {int_mod} {is_neg}")
                    return str(-int_mod) if is_neg else str(int_mod)
                case '<':
                    return icfp_bool(int(x) < int(y))
                case '>':
                    return icfp_bool(int(x) > int(y))
                case '=':
                    #return icfp_bool(int(x) == int(y))
                    return x == y
                case '|':
                    return icfp_bool(str_to_bool(x) or str_to_bool(y))
                case '&':
                    return icfp_bool(str_to_bool(x) and str_to_bool(y))
                case '.':
                    return x + y
                case 'T':
                    return y[:int(x)]
                case 'D':
                    return y[int(x):]
                case _:
                    err(f'bad B body "{body}" in "{token}"')
                    return ''
        case '?':
            cond_icfp, rest = extract_icfp(rest)
            yes, rest = extract_icfp(rest)
            no, rest = extract_icfp(rest)
            b = evaluate_icfp(cond_icfp, vars, later)
            if str_to_bool(b):
                return evaluate_icfp(yes, vars, later)
            else:
                return evaluate_icfp(no, vars, later)
        case 'L':
            var_name = body
            var_icfp = later.pop()
            vars[var_name] = var_icfp
            return evaluate_icfp(rest, vars, later)
        case 'v':
            if body not in vars:
                err(f'no v{body} to substitute')
            var_icfp = vars[body]
            return evaluate_icfp(var_icfp, vars)
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

def show(text: str) -> str:
    """
    Send text to the cult.
    Just return the result (no evaluate!).
    """
    program = [f'STR {text}']
    r = post(assemble(program))
    return r.text

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
