import pytest
from hypothesis import (
    given,
    example,
)
from hypothesis import strategies as st

from web3.utils.string import force_text


@pytest.mark.parametrize(
    'initial_value,tail,expected',
    (
        ('', 'tail', 'tail'),
        ('head', 'tail', 'headtail'),
    )
)
def test_string_concatenation(chain, test_string_lib, initial_value, tail, expected):
    if initial_value:
        chain.wait.for_receipt(test_string_lib.transact().set(initial_value))

    assert test_string_lib.call().value() == initial_value

    chain.wait.for_receipt(test_string_lib.transact().concatString(tail))

    assert test_string_lib.call().value() == expected


@given(
    initial_value=st.binary(),
    tail=st.integers(min_value=0, max_value=2**256 - 1),
)
@example(initial_value=b'', tail=0)
@example(initial_value=b'', tail=1)
@example(initial_value=b'', tail=10)
@example(initial_value=b'', tail=101)
@example(initial_value=b'', tail=256)
def test_fuzzing_uint_concatenation(chain, test_string_lib, initial_value, tail):
    chain.wait.for_receipt(test_string_lib.transact().reset())

    if initial_value:
        chain.wait.for_receipt(test_string_lib.transact().set(initial_value))

    assert test_string_lib.call().value() == force_text(initial_value)

    chain.wait.for_receipt(test_string_lib.transact().concatUInt(tail))

    expected = force_text(initial_value) + str(tail)

    assert test_string_lib.call().value() == expected
