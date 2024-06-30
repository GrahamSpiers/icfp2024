# icfp common stuff package

import requests
from sys import exit


CULT_URL = 'https://boundvariable.space/communicate'

TEAM_AUTHORIZATION = 'Bearer 921df178-ab9d-43a9-ad36-fc844c4647b6'

S_ASCII = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n'''

I_BASE = 94
ZERO_INDEX = 33

# B

def tok_b_to_bool(tok_b: str) -> bool:
    return tok_b == 'T'

def bool_to_tok_b(tf: bool) -> str:
    return 'T' if tf else 'F'

def str_to_bool(s: str) -> bool:
    return s == 'true'

def icfp_bool(tf: bool) -> str:
    return 'true' if tf else 'false'


# I

def tok_i_to_int(tok_i: str) -> int:
    return base94_to_int(tok_i[1:])

def int_to_tok_i(i: int) -> str:
    return 'I' + str(int_to_str(i))

def base94_to_int(s: str) -> int:
    i = 0
    for ch in s:
        i *= I_BASE
        i += ord(ch) - ZERO_INDEX
    return i

def int_to_str(i: int) -> str:
    result = ''
    if i == 0:
        return '!'
    while i:
        d = i % I_BASE
        #i -= d
        i //= I_BASE
        result += S_ASCII[d]
    return result[::-1]

def s_str_to_int(s: str) -> int:
    i = 0
    for ch in s:
        i *= I_BASE
        index = S_ASCII.index(ch)
        i += index
    return i

def int_to_base94(i: int) -> str:
    if i == 0:
        return '!'
    s = ''
    while i > 0:
        s += chr(ZERO_INDEX + i % I_BASE)
        i //= I_BASE
    return s[::-1]

# S

def tok_s_to_str(tok_s: str) -> str:
    return s_to_str(tok_s[1:])

def str_to_tok_s(s: str) -> str:
    return 'S' + ''.join([
        to_s(ascii_ch)
        for ascii_ch in s
    ])

def to_s(ascii_ch: str) -> str:
    index = S_ASCII.index(ascii_ch)
    return chr(ZERO_INDEX + index)

def s_to_str(s: str) -> str:
    return ''.join([
        S_ASCII[ord(ch)-ZERO_INDEX]
        for ch in s
    ])


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


# Evaluator 3

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
        case 'I': return str(base94_to_int(body))
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
                    return str(s_str_to_int(x))
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
                    return icfp_bool(x == y)
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

def tokenize(icfp: str) -> list[str]:
    return icfp.split(sep=' ')


# Communications

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

def post(message: str):
    r = requests.post(
            CULT_URL,
            headers={'Authorization': TEAM_AUTHORIZATION},
            data=message)
    if r.status_code != 200:
        err(f'bad http post status {r.status_code}')
    return r


# Errors

def err(what: str, code: int = 1) -> None:
    print(f"error: {what}")
    exit(code)
