# hypermi.py
# A hyperspeed macro interpreter.

import operator
from icfp.error import err
from icfp.tfis import tok_i_to_int, s_to_str, base94_to_int, int_to_base94


def hyper_evaluate(icfp_str: str) -> str:
    icfp = hyper_compile(icfp_str)
    print(icfp.show())
    result = icfp.run()
    if isinstance(result, str):
        return s_to_str(result)
    else:
        return str(result)


class ICFP:
    def __init__(self, token: str = '') -> None:
        self.token = token
        self.sub: list[any] = []
    def extract(self, typed: list[any]) -> list[any]:
        self.sub.append(typed[0])
        if isinstance(typed[0], ICFP):
            return typed[0].extract(typed[1:])
        return typed[1:]
    def run(self) -> any:
        #print(f'ICFP.run {scope} {later_stack}')
        return eval(self.sub[0])
    def substitute(self, key: str, lambda_icfp: any) -> None:
        #print(f'replacing {key} with {_show(lambda_icfp)}')
        if isinstance(self, v) and self.key == key:
            self.sub.append(lambda_icfp)
        else:
            for sub in self.sub:
                if isinstance(sub, ICFP):
                    sub.substitute(key, lambda_icfp)
    def show(self) -> str:
        return _show(self.sub[0])


def eval(what: any) -> any:
    if isinstance(what, ICFP):
        return what.run()
    else:
        #print(f'-> {what}')
        return what


def _show(what: any) -> str:
    if isinstance(what, ICFP):
        return what.show()
    else:
        return str(what)


class Unary(ICFP):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        match token[1:]:
            case '-':
                self.op = operator.neg
            case '!':
                self.op = lambda tf: not tf
            case '#':
                self.op = base94_to_int
            case '$':
                self.op = int_to_base94
            case _:
                err(f'bad unary token "{token}"')
    def extract(self, typed: list[any]) -> list[any]:
        self.sub.append(typed[0])
        if isinstance(typed[0], ICFP):
            return typed[0].extract(typed[1:])
        return typed[1:]
    def run(self) -> any:
        #print(f'Unary.run {scope} {later_stack}')
        x = eval(self.sub[0])
        #print(f'{self.token}({x})')
        return self.op(x)
    def show(self) -> str:
        return f'{self.token}({_show(self.sub[0])})'


class Binary(ICFP):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.is_apply = False
        match token[1:]:
            case '+':
                self.op = operator.add
            case '-':
                self.op = operator.sub
            case '*':
                self.op = operator.mul
            case '/':
                self.op = bin_div
            case '%':
                self.op = bin_mod
            case '<':
                self.op = operator.lt
            case '>':
                self.op = operator.gt
            case '=':
                self.op = operator.eq
            case '|':
                self.op = operator.or_
            case '&':
                self.op = operator.and_
            case '.':
                self.op = operator.add
            case 'T':
                self.op = bin_take
            case 'D':
                self.op = bin_drop
            case '$':
                self.is_apply = True
            case _:
                err(f'bad binary token "{token}"')
    def extract(self, typed: list[any]) -> list[any]:
        self.sub.append(typed[0])
        rest = typed[1:]
        if isinstance(typed[0], ICFP):
            rest = typed[0].extract(rest)
        self.sub.append(rest[0])
        rest = rest[1:]
        if isinstance(self.sub[-1], ICFP):
            rest = self.sub[-1].extract(rest)
        return rest
    def run(self) -> any:
        if self.is_apply:
            #print(f'Apply {scope} {later_stack}')
            lmbda = eval(self.sub[0])
            if isinstance(lmbda.sub[0], ICFP):
                lmbda.sub[0].substitute(lmbda.key, self.sub[1])
            return eval(lmbda.sub[0])
        #print(f'Binary.run {scope} {later_stack}')
        x = eval(self.sub[0])
        y = eval(self.sub[1])
        #print(f'{self.token}({x}, {y})')
        return self.op(x, y)
    def show(self) -> str:
        return f'{self.token} ({_show(self.sub[0])}, {_show(self.sub[1])})'

def bin_div(x: int, y: int) -> int:
    is_neg = (x < 0 and y > 0) or (x > 0 and y < 0)
    int_div = abs(x) // abs(y)
    #print(f"{int_x} {int_y} {int_div} {is_neg}")
    return -int_div if is_neg else int_div

def bin_mod(x: int, y: int) -> int:
    is_neg = (x < 0 and y > 0) or (x > 0 and y < 0)
    int_mod = abs(x) % abs(y)
    #print(f"{int_x} {int_y} {int_mod} {is_neg}")
    return -int_mod if is_neg else int_mod

def bin_take(x: int, y: str) -> str:
    return y[:x]

def bin_drop(x: int, y: str) -> str:
    return y[x:]

class If(ICFP):
    def __init__(self, token: str) -> None:
        super().__init__(token)
    def extract(self, typed: list[any]) -> list[any]:
        self.sub.append(typed[0])
        rest = typed[1:]
        if isinstance(typed[0], ICFP):
            rest = typed[0].extract(rest)
        self.sub.append(rest[0])
        rest = rest[1:]
        if isinstance(self.sub[-1], ICFP):
            rest = self.sub[-1].extract(rest)
        self.sub.append(rest[0])
        rest = rest[1:]
        if isinstance(self.sub[-1], ICFP):
            rest = self.sub[-1].extract(rest)
        return rest
    def run(self) -> any:
        #print(f'If.run {scope} {later_stack}')
        tf = eval(self.sub[0])
        #print(f'{self.token}({tf})')
        if tf:
            return eval(self.sub[1])
        else:
            return eval(self.sub[2])
    def show(self) -> str:
        return f'{self.token}({_show(self.sub[0])} {_show(self.sub[1])} {_show(self.sub[2])})'


class Lambda(ICFP):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.key = token[1:]
    def extract(self, typed: list[any]) -> list[any]:
        self.sub.append(typed[0])
        rest = typed[1:]
        if isinstance(typed[0], ICFP):
            rest = typed[0].extract(rest)
        #print(self.show())
        return rest
    def run(self) -> any:
        return self
    def show(self) -> str:
        return f'{self.token} [{_show(self.sub[0])}]'

class v(ICFP):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.key = token[1:]
    def extract(self, typed: list[any]) -> list[any]:
        return typed
    def run(self) -> any:
        if not self.sub:
            err(f'{self.token} not replaced')
        return eval(self.sub[0])
    def show(self) -> str:
        return self.token


def hyper_compile(icfp_str: str) -> ICFP:
    tokens = icfp_str.split(' ')
    typed = as_types(tokens)
    #print(typed)
    icfp_top = ICFP()
    icfp_top.extract(typed)
    #print(f'ICFP={icfp_top.show()}')
    return icfp_top

def as_types(tokens: str) -> list[any]:
    return [
        make_type(token)
        for token in tokens
    ]

def make_type(token: str) -> any:
    match token[0]:
        case 'T': return True
        case 'F': return False
        case 'I': return tok_i_to_int(token)
        case 'S': return token[1:] # STILL ICFP!
        case 'U': return Unary(token)
        case 'B': return Binary(token)
        case '?': return If(token)
        case 'L': return Lambda(token)
        case 'v': return v(token)
        case _: err(f'make_type: unknown token "{token}"')
