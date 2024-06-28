# icfp common stuff package

import requests
from sys import exit


CULT_URL = 'https://boundvariable.space/communicate'

TEAM_AUTHORIZATION = 'Bearer 921df178-ab9d-43a9-ad36-fc844c4647b6'

S_ASCII = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n'''


def eval(icfp: str) -> str:
    print(f"icfp:({icfp})")
    return '\n'.join([
        eval_token(token)
        for token in tokenize(icfp)
    ])

def eval_token(token: str) -> str:
    print(f"token({token})")
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


def err(what: str, code: int = 1) -> None:
    print(f"error: {what}")
    exit(code)


def post(message: str) -> None:
    return requests.post(
            CULT_URL,
            headers={'Authorization': TEAM_AUTHORIZATION},
            data=message)
