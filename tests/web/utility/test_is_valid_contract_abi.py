import pytest
import json

from func_sig_registry.utils.abi import (
    is_valid_contract_abi,
)


CONSTRUCTOR_ONLY = json.loads('[{"inputs":[{"name":"a","type":"address"},{"name":"b","type":"uint256"}],"type":"constructor"}]')

SINGLE_FUNCTION = json.loads('[{"constant":false,"inputs":[{"name":"a","type":"address"},{"name":"b","type":"uint256"}],"name":"f","outputs":[],"type":"function"}]')

SINGLE_FUNCTION_WITH_RETURN = json.loads('[{"constant":false,"inputs":[{"name":"a","type":"address"},{"name":"b","type":"uint256"}],"name":"f","outputs":[{"name":"","type":"uint256"},{"name":"","type":"address"}],"type":"function"}]')

SINGLE_EVENT = json.loads('[{"anonymous":false,"inputs":[],"name":"F","type":"event"}]')

SOME_OF_EACH = json.loads('[{"constant":false,"inputs":[],"name":"f","outputs":[],"type":"function"},{"inputs":[],"type":"constructor"},{"anonymous":false,"inputs":[],"name":"E","type":"event"}]')

SOME_OF_EACH_AND_THREE_FUNCTIONS = json.loads('[{"constant":false,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"int256"},{"name":"","type":"address"}],"name":"c","outputs":[],"type":"function"},{"constant":false,"inputs":[],"name":"f","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"","type":"int256"},{"name":"","type":"int256"}],"name":"b","outputs":[],"type":"function"},{"inputs":[],"type":"constructor"},{"anonymous":false,"inputs":[],"name":"E","type":"event"}]')

SINGLE_EVENT_INDEXED = [{
    "type": "event",
    "inputs": [
        {"name": "a", "type": "uint256", "indexed": True},
        {"name": "b", "type": "bytes32", "indexed": False}
        ],
    "name": "foo",
    "anonymous": False
}]

MISSING_INDEXED_EVENT = [{
    "type": "event",
    "inputs": [
        {"name": "a", "type": "uint256"},
        {"name": "b", "type": "bytes32", "indexed": False}
        ],
    "name": "foo",
    "anonymous": False
}]

INCORRECT_INDEXED_TYPE = [{
    "type": "event",
    "inputs": [
        {"name": "a", "type": "uint256", "indexed": "True"},
        {"name": "b", "type": "bytes32", "indexed": False}
        ],
    "name": "foo",
    "anonymous": False
}]

MISSING_FUNCTION_NAME = [{
    'constant': True,
    'inputs': [],
    'outputs': [],
    'type': 'function',
}]

MISSING_FUNCTION_TYPE = [{
    'constant': True,
    'name': 'foo',
    'inputs': [],
    'outputs': [],
}]

ABI_TUPLE_ARG = json.loads('[{"constant":false,"inputs":[{"components":[{"internalType":"int256","name":"x","type":"int256"},{"internalType":"int256","name":"y","type":"int256"}],"internalType":"struct Test2.Test","name":"a","type":"tuple"}],"name":"myFun","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# from 0x4f833a24e1f95d70f028921e27040ca56e09ab0b mainnet address:
# https://github.com/pipermerriam/ethereum-function-signature-registry/issues/37
ABI_GET_ORDERS_INFO = json.loads('[{"constant":true,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"}],"name":"getOrdersInfo","outputs":[{"components":[{"name":"orderStatus","type":"uint8"},{"name":"orderHash","type":"bytes32"},{"name":"orderTakerAssetFilledAmount","type":"uint256"}],"name":"","type":"tuple[]"}],"payable":false,"stateMutability":"view","type":"function"}]')


@pytest.mark.parametrize(
    'contract_abi,expected',
    (
        # obviously invalid
        ([1], False),
        (['1'], False),
        ([[]], False),
        ([True], False),
        # empty
        ([], True),
        # actual ABI definitions
        (CONSTRUCTOR_ONLY, True),
        (SINGLE_FUNCTION, True),
        (SINGLE_FUNCTION_WITH_RETURN, True),
        (SINGLE_EVENT, True),
        (SOME_OF_EACH, True),
        (SOME_OF_EACH_AND_THREE_FUNCTIONS, True),
        # complex ABI definitions
        (ABI_TUPLE_ARG, True),
        (ABI_GET_ORDERS_INFO, True),
        # bad definitions
        (MISSING_FUNCTION_NAME, False),
        (MISSING_FUNCTION_TYPE, False),
        (MISSING_INDEXED_EVENT, False),
        (INCORRECT_INDEXED_TYPE, False),
        # event with indexed
        (SINGLE_EVENT_INDEXED, True),

    ),
)
def test_is_valid_contract_abi(contract_abi, expected):
    actual = is_valid_contract_abi(contract_abi)
    assert actual is expected
