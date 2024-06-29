from icfp.icfp import eval, assemble, evaluate
def test_hello_world() -> None:
    """
    SB%,,/}Q/2,$_
    is
    Hello World!
    """
    assert 'Hello World!' == eval('SB%,,/}Q/2,$_')


def test_assemble_str() -> None:
    """
    The reverse of eval(s)
    """
    assert 'SB%,,/}Q/2,$_' == assemble(['STR Hello World!'])


def test_token_lists() -> None:
    tests = [
        ('SB%,,/}Q/2,$_', 'Hello World!'),
        ('T', 'true'),
        ('F', 'false'),
        ('I$', '3'),
        ('I#', '2'),
        ('I/6', '1337'),
        ('I!', '0'),
        ('U- I$', '-3'),
        ('U- I(', '-7'),
        ('U! T', 'false'),
        #('U# S4%34', '15818151'),
        ('U$ I4%34', 'test'),
        ('B+ I# I$', '5'),
        ('B- I$ I#', '1'),
        ('B* I$ I#', '6'),
        ('B/ U- I( I#', '-3'),
        ('B% U- I( I#', '-1'),
        ('B< I$ I#', 'false'),
        ('B> I$ I#', 'true'),
        ('B= I$ I#', 'false'),
        ('B= I$ I$', 'true'),
        ('B| T F', 'true'),
        ('B| T T', 'true'),
        ('B| F F', 'false'),
        ('B& T F', 'false'),
        ('B& T T', 'true'),
        ('B. S4% S34', 'test'),
        ('BT I$ S4%34', 'tes'),
        ('BD I$ S4%34', 't'),
        #('', ''),
    ]
    for test in tests:
        print(f'{test[0]} -> {test[1]}')
        result = evaluate(test[0])
        assert test[1] == result, f'expected "{test[1]}" got "{result}" from "{test[0]}"'

