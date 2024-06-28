from icfp.icfp import eval, assemble

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