import pytest

from func_sig_registry.utils.solidity import (
    is_raw_function_signature,
)


@pytest.mark.parametrize(
    'raw_signature',
    (
        'function foo()',
        'function foo(int a, int b, int c, int d)',
        'function foo(address v)',
        'function   foo  ( address v )',
        'function foo(address v,\nint i)',
        'function foo(\naddress   v,\nint i\n)',
        'function foo (address v)',
        'function foo(address v, int i)',
        'function foo(address v,int i)',
        'function foo(address[] v, int i)',
        'function foo(address[2] v, int i)',
        'function foo(address[2][][3] v, int i)',
    )
)
def test_is_raw_function_signature_for_valid_signatures(raw_signature):
    assert is_raw_function_signature(raw_signature) is True


@pytest.mark.parametrize(
    'invalid_signature',
    (
        'foo()',
        'function 3()',
        'function foo(',
        'function foo)',
        'function()',
        'functionfoo()',
        'function foo(int)',
        'function foo(int255 a)',
        'function foo(int a int b)',
        'function foo(int a, int b,)',
        'function foo(,int a)',
        'function foo(int[ a)',
        'function foo(int] a)',
    )
)
def test_is_raw_function_signature_for_invalid_signatures(invalid_signature):
    assert is_raw_function_signature(invalid_signature) is False
