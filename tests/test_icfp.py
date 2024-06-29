from icfp.icfp import assemble, tokenize, evaluate


def test_hello_world() -> None:
    """
    SB%,,/}Q/2,$_
    is
    Hello World!
    """
    assert 'Hello World!' == evaluate('SB%,,/}Q/2,$_')


def test_assemble_str() -> None:
    """
    The reverse of evaluate(s)
    """
    assert 'SB%,,/}Q/2,$_' == assemble(['STR Hello World!'])


def test_evaluate() -> None:
    tests = [
        ('SB%,,/}Q/2,$_', 'Hello World!'),
        ('T', 'true'),
        ('F', 'false'),
        ('I$', '3'),
        ('I#', '2'),
        ('I/6', '1337'),
        ('I4%34', '15818151'),
        ('I!', '0'),
        ('U- I$', '-3'),
        ('U- I(', '-7'),
        ('U! T', 'false'),
        ('S4%34', 'test'),
        ('U# S4%34', '15818151'),
        ('U$ I4%34', 'test'),
        ('B+ I# I$', '5'),
        ('B- I$ I#', '1'),
        ('B* I$ I#', '6'),
        ('B/ U- I( I#', '-3'),
        ('B/ I( I#', '3'),
        ('B% U- I( I#', '-1'),
        ('B% I( I#', '1'),
        ('B< I$ I#', 'false'),
        ('B< I# I$', 'true'),
        ('B> I$ I#', 'true'),
        ('B> I# I$', 'false'),
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
        ('S./', 'no'),
        ('S9%3', 'yes'),
        ('? B> I# I$ S9%3 S./', 'no'),
        ('? B= I# I$ S9%3 S./', 'no'),
        ('? B< I# I$ S9%3 S./', 'yes'),
        ('B. SB%,,/ S}Q/2,$_', 'Hello World!'),
        #('', ''),
    ]
    for test in tests:
        print(f'{test[0]} -> {test[1]}')
        result = evaluate(test[0])
        assert test[1] == result, f'expected "{test[1]}" got "{result}" from "{test[0]}"'


def test_lambda() -> None:
    tests = [
        #('I-', '12'),
        #("B+ I' I'", '12'),
        ('B$ Lx B+ vx vx I$', '6'),
        ('B$ Lx B+ I$ vx I$', '6'),
        ('B$ Lx B+ vx I$ I$', '6'),
        #("B+ I' B* I$ I#", '12'),
        #('B* I$ I#', '6'),
        #("I'", '6'),
        ('B$ L" v" I-', '12'),
        ("""B$ L" B+ v" v" I'""", '12'),
        ('''B$ L" B+ v" v" B* I$ I#''', '12'),
        #('SB%,,/}Q/2,$_', 'Hello World!'),
        ('B$ L$ v$ I#', '2'),
        ('B$ B$ L# L$ v# SB%,,/}Q/2,$_ IK', 'Hello World!'),
        ('B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK', 'Hello World!'),
    ]
    for test in tests:
        print(f'{test[0]} -> {test[1]}')
        result = evaluate(test[0])
        assert test[1] == result, f'expected "{test[1]}" got "{result}" from "{test[0]}"'

#def test_limits() -> None:
#    # This uses 109 beta reductions...
#    # And lambdas...
#    result = evaluate('B$ B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L" L# ? B= v# I! I" B$ L$ B+ B$ v" v$ B$ v" v$ B- v# I" I%')
#    assert '16' == result