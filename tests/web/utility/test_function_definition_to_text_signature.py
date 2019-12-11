import json

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

ABI_TUPLE_ARG = json.loads('{"constant":false,"inputs":[{"components":[{"internalType":"int256","name":"x","type":"int256"},{"internalType":"int256","name":"y","type":"int256"}],"internalType":"struct Test2.Test","name":"a","type":"tuple"}],"name":"myFun","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}')

# from 0x4f833a24e1f95d70f028921e27040ca56e09ab0b mainnet address:
# https://github.com/pipermerriam/ethereum-function-signature-registry/issues/37
ABI_GET_ORDERS_INFO = json.loads('{"constant":true,"inputs":[{"components":[{"name":"makerAddress","type":"address"},{"name":"takerAddress","type":"address"},{"name":"feeRecipientAddress","type":"address"},{"name":"senderAddress","type":"address"},{"name":"makerAssetAmount","type":"uint256"},{"name":"takerAssetAmount","type":"uint256"},{"name":"makerFee","type":"uint256"},{"name":"takerFee","type":"uint256"},{"name":"expirationTimeSeconds","type":"uint256"},{"name":"salt","type":"uint256"},{"name":"makerAssetData","type":"bytes"},{"name":"takerAssetData","type":"bytes"}],"name":"orders","type":"tuple[]"}],"name":"getOrdersInfo","outputs":[{"components":[{"name":"orderStatus","type":"uint8"},{"name":"orderHash","type":"bytes32"},{"name":"orderTakerAssetFilledAmount","type":"uint256"}],"name":"","type":"tuple[]"}],"payable":false,"stateMutability":"view","type":"function"}')


@pytest.mark.parametrize(
    'fn_abi,expected',
    (
        (ABI_NO_ARGS, 'foo()'),
        (ABI_SINGLE_ARG, 'foo(int256)'),
        (ABI_TWO_ARGS, 'foo(address,uint256)'),
        (ABI_TUPLE_ARG, 'myFun((int256,int256))'),
        (ABI_GET_ORDERS_INFO, 'getOrdersInfo((address,address,address,address,uint256,uint256,uint256,uint256,uint256,uint256,bytes,bytes)[])'),
    ),
)
def test_function_definition_to_text_signature(fn_abi, expected):
    actual = function_definition_to_text_signature(fn_abi)
    assert actual == expected
