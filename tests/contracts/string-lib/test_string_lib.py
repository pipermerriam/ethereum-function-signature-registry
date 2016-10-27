import string

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


ALPHA_NUMERIC_CHARS = set('_' + string.digits + string.ascii_letters)


def test_char_lib(char_lib):
    for character in map(chr, range(256)):
        is_digit = character in string.digits
        is_alpha = character in string.ascii_letters
        is_lower = character in string.ascii_lowercase
        is_upper = character in string.ascii_uppercase
        is_underscore = character == "_"
        is_alpha_numeric = is_alpha or is_digit

        assert char_lib.call().isUnderscore(character) is is_underscore
        assert char_lib.call().isAlpha(character) is is_alpha
        assert char_lib.call().isDigit(character) is is_digit
        assert char_lib.call().isAlphaLower(character) is is_lower
        assert char_lib.call().isAlphaUpper(character) is is_upper
        assert char_lib.call().isAlphaNumeric(character) is is_alpha_numeric


@given(binary_text=st.binary())
def test_stringlib_alpha_numeric(string_lib, binary_text):
    text = force_text(binary_text)
    is_alpha_numeric = all((
        c in ALPHA_NUMERIC_CHARS for c in text
    ))

    assert string_lib.call().isAlphaNumeric(text) is is_alpha_numeric
