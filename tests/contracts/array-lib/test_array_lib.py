import pytest


@pytest.mark.parametrize(
    'is_dynamic,size,expected',
    (
        (False, 0, '[0]'),
        (False, 1, '[1]'),
        (False, 123, '[123]'),
        (False, 987654321, '[987654321]'),
        (True, 0, '[]'),
        (True, 1, '[]'),
    ),
)
def test_array_lib_repr(chain, test_array_lib, is_dynamic, size, expected):
    chain.wait.for_receipt(test_array_lib.transact().set(is_dynamic, size))

    assert test_array_lib.call().repr() == expected
