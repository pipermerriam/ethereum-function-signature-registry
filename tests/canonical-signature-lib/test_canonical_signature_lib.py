import pytest

from eth_abi.abi import process_type

from web3.utils.string import (
    force_text,
)

from func_sig_registry.utils.abi import (
    make_4byte_signature,
    function_definition_to_text_signature,
)
from func_sig_registry.utils.solidity import (
    is_canonical_function_signature,
)


class DataTypes(object):
    Null = 0
    Address = 1
    Bool = 2
    UInt = 3
    Int = 4
    BytesFixed = 5
    BytesDynamic = 6
    String = 7

    @classmethod
    def from_string(cls, _type):
        base, sub, arrlist = process_type(_type)
        if base == 'bytes':
            if sub:
                return cls.BytesFixed
            else:
                return cls.BytesDynamic
        elif base == 'string':
            return cls.String
        elif base == 'int':
            return cls.Int
        elif base == 'uint':
            return cls.UInt
        elif base == 'bool':
            return cls.Bool
        elif base == 'address':
            return cls.Address
        else:
            raise ValueError("Unknown type: {0}".format(_type))


def function_definition_to_kwargs(function_abi):
    """
    uint[] dataTypes,
    uint[] subs,
    bool[] arrListsDynamic,
    uint[] arrListsSize) returns (bool) {
    """
    kwargs = {}
    kwargs = {
        '_name': function_abi['name'],
        'dataTypes': [],
        'subs': [],
        'arrListsDynamic': [],
        'arrListsSize': [],
    }
    for argument_abi in function_abi['inputs']:
        kwargs['dataTypes'].append(DataTypes.from_string(argument_abi['type']))
        base, sub, arrlist = process_type(argument_abi['type'])
        if sub:
            kwargs['subs'].append(int(sub))
        else:
            kwargs['subs'].append(0)

        for arr_value in arrlist:
            kwargs['arrListsDynamic'].append(bool(arr_value))
            if arr_value:
                kwargs['arrListsSize'].append(arr_value[0])
            else:
                kwargs['arrListsSize'].append(0)

    return kwargs


ABI_A = {
    'name': 'foo',
    'inputs': [],
    'type': 'function',
}
ABI_B = {
    'name': 'foo',
    'inputs': [
        {'type': 'bytes32'},
    ],
    'type': 'function',
}
ABI_C = {
    'name': 'foo',
    'inputs': [
        {'type': 'bytes32'},
        {'type': 'bytes32[][24][]'},
    ],
    'type': 'function',
}
ABI_D = {
    'name': 'fooBar',
    'inputs': [
        {'type': 'uint256'},
        {'type': 'address'},
        {'type': 'string[3][]'},
        {'type': 'string'},
        {'type': 'address[2]'},
        {'type': 'bytes'},
        {'type': 'int8'},
        {'type': 'int256'},
        {'type': 'bytes[]'},
        {'type': 'bool'},
        {'type': 'bool[3][2]'},
        {'type': 'bytes32[][24][]'},
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
