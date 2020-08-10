import json

import pytest

from func_sig_registry.utils.abi import (
    event_definition_to_text_signature,
)


ABI_SINGLE_ARG = {
    "inputs": [
        {"name": "a", "type": "int256", "indexed" : False},
    ],
    "name": "foo",
    "type": "event",
    "anonymous": False,
}


ABI_TWO_ARGS = {
    "inputs": [
        {"name": "a", "type": "address", "indexed" : True},
        {"name": "b", "type": "uint256", "indexed" : False},
    ],
    "name": "foo",
    "type": "event",
    "anonymous": False,
}

ABI_TUPLE_ARG = json.loads('{"inputs":[{"indexed":false, "components":[{"internalType":"int256","name":"x","type":"int256"},{"internalType":"int256","name":"y","type":"int256"}],"internalType":"struct Test2.Test","name":"a","type":"tuple"}],"name":"myEvent","type":"event"}')

ABI_GET_ORDERS_INFO = json.loads('{"inputs":[{"indexed":false, "components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"}],"name":"OrdersInfo","type":"event"}')


@pytest.mark.parametrize(
    'fn_abi,expected',
    (
        (ABI_SINGLE_ARG, 'foo(int256)'),
        (ABI_TWO_ARGS, 'foo(address indexed,uint256)'),
        (ABI_TUPLE_ARG, 'myEvent((int256,int256))'),
        (ABI_GET_ORDERS_INFO, 'OrdersInfo((address,address,address,address,uint256,uint256,uint256,uint256,uint256,uint256,bytes,bytes)[])'),
    ),
)
def test_function_definition_to_text_signature(fn_abi, expected):
    actual = event_definition_to_text_signature(fn_abi)
    assert actual == expected
