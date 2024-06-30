# tfis
# ICFP T F I and S

S_ASCII = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n'''

I_BASE = 94
ZERO_INDEX = 33

# TF

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


