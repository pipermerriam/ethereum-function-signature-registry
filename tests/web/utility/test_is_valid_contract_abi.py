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
        # bad definitions
        (MISSING_FUNCTION_NAME, False),
        (MISSING_FUNCTION_TYPE, False),
    ),
)
def test_is_valid_contract_abi(contract_abi, expected):
    actual = is_valid_contract_abi(contract_abi)
    assert actual is expected
