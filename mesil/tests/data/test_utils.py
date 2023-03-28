from mesil.data.utils import (has_float_starter, regex_split,
                              wrap_list)


def test_check_float_starter():
    cases = ['File Name:	DIC3H', '0.000000	28.844490	9.995243	1.903549']
    assert [has_float_starter(case) for case in cases] == [False, True]


def test_regex_split():
    cases = [
        '0.000000	28.844490	9.995243	1.903549',
        'Labels,EmScan5_DIC3H_3scan',
    ]
    assert [len(regex_split(case)) for case in cases] == [4, 2]


def test_wrap_list():
    example = ['cat', 'dog', 'bear']
    assert wrap_list(example) == [['cat'], ['dog'], ['bear']]
