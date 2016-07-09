import pytest

from func_sig_registry.utils.solidity import (
    to_canonical_type,
    STATIC_TYPES,
)


@pytest.mark.parametrize(
    'input_type,expected',
    (
        ('uint', 'uint256'),
        ('int', 'int256'),
        ('byte', 'bytes1'),
    )
)
def test_converts_shorthand_types_to_canonical_types(input_type, expected):
    actual = to_canonical_type(input_type)
    assert actual == expected


@pytest.mark.parametrize(
    'input_type',
    STATIC_TYPES,
)
def test_preserves_canonical_representations(input_type):
    assert to_canonical_type(input_type) == input_type
