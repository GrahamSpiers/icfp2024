# Errors

from sys import exit


def err(what: str, code: int = 1) -> None:
    print(f"error: {what}")
    exit(code)
