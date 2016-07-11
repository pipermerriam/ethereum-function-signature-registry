import pytest

from func_sig_registry.utils.abi import (
    function_definition_to_text_signature,
)


ABI_NO_ARGS = {
    "constant": False,
    "inputs": [],
    "name": "foo",
    "outputs": [],
    "type": "function",
}


ABI_SINGLE_ARG = {
    "constant": False,
    "inputs": [
        {"name": "a", "type": "int256"},
    ],
    "name": "foo",
    "outputs": [],
    "type": "function",
}


ABI_TWO_ARGS = {
    "constant": False,
    "inputs": [
        {"name": "a", "type": "address"},
        {"name": "b", "type": "uint256"},
    ],
    "name": "foo",
    "outputs": [],
    "type": "function",
}


@pytest.mark.parametrize(
    'fn_abi,expected',
    (
        (ABI_NO_ARGS, 'foo()'),
        (ABI_SINGLE_ARG, 'foo(int256)'),
        (ABI_TWO_ARGS, 'foo(address,uint256)'),
    ),
)
def test_function_definition_to_text_signature(fn_abi, expected):
    actual = function_definition_to_text_signature(fn_abi)
    assert actual == expected
