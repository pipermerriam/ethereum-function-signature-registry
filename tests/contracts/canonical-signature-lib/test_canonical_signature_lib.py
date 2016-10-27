import pytest

from web3.utils.string import (
    force_text,
)

from func_sig_registry.utils.signature_db import (
    function_definition_to_kwargs,
)
from func_sig_registry.utils.abi import (
    make_4byte_signature,
    function_definition_to_text_signature,
)
from func_sig_registry.utils.solidity import (
    is_canonical_function_signature,
)


ABI_A = {
    'name': 'foo',
    'inputs': [],
    'type': 'function',
}
ABI_B = {
    'name': 'Foo_123',
    'inputs': [
        {'type': 'bytes32'},
    ],
    'type': 'function',
}
ABI_C = {
    'name': '_____',
    'inputs': [
        {'type': 'bytes32'},
        {'type': 'bytes32[][24][]'},
        {'type': 'string[3][]'},
    ],
    'type': 'function',
}
ABI_D = {
    'name': 'fooBar',
    'inputs': [
        {'type': 'uint256'},
        {'type': 'address'},
        {'type': 'string'},
        {'type': 'address[2]'},
        {'type': 'int8'},
        {'type': 'bool'},
        {'type': 'bool[3][2]'},
    ],
    'type': 'function',
}


@pytest.mark.parametrize(
    'abi',
    (
        ABI_A,
        ABI_B,
        ABI_C,
        ABI_D,
    ),
)
def test_cannonical_signature_lib_to_string(chain, test_canonical_signature_lib, abi):
    init_kwargs = function_definition_to_kwargs(abi)
    chain.wait.for_receipt(test_canonical_signature_lib.transact().set(
        **init_kwargs
    ))

    assert test_canonical_signature_lib.call().isValid()

    expected_signature = function_definition_to_text_signature(abi)
    expected_selector = force_text(make_4byte_signature(expected_signature))

    actual_signature = test_canonical_signature_lib.call().repr()
    actual_selector = test_canonical_signature_lib.call().selector()

    assert actual_signature == expected_signature
    assert actual_selector == expected_selector

    assert is_canonical_function_signature(actual_signature)


BAD_ABI_A = {
    'name': '9foo',  # fn names can't start with numbers
    'inputs': [],
    'type': 'function',
}
BAD_ABI_B = {
    'name': 'foo-bar',  # fn names can't have dashes.
    'inputs': [],
    'type': 'function',
}
BAD_ABI_C = {
    'name': 'foo bar',  # fn names can't have spaces.
    'inputs': [],
    'type': 'function',
}
BAD_ABI_D = {
    'name': '',  # fn names can't be empty
    'inputs': [],
    'type': 'function',
}


@pytest.mark.parametrize(
    'abi',
    (
        BAD_ABI_A,
        BAD_ABI_B,
        BAD_ABI_C,
        BAD_ABI_D,
    ),
)
def test_canonical_signature_lib_validation(chain, test_canonical_signature_lib, abi):
    init_kwargs = function_definition_to_kwargs(abi)
    chain.wait.for_receipt(test_canonical_signature_lib.transact().set(
        **init_kwargs
    ))

    assert test_canonical_signature_lib.call().isValid() is False
