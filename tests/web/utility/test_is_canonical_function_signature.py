import pytest

from func_sig_registry.utils.solidity import (
    is_canonical_function_signature,
)


@pytest.mark.parametrize(
    'canonical_signature',
    (
        'a()',
        'a1()',
        'abc123_()',
        '_abc123()',
        'foo(int256,int256)',
        'foo(int256)',
        'foo(address)',
        'foo(address[])',
        'foo(address[2])',
        'foo(address[2][][3])',
    )
)
def test_is_canonical_function_signature_for_valid_signatures(canonical_signature):
    assert is_canonical_function_signature(canonical_signature) is True


@pytest.mark.parametrize(
    'invalid_signature',
    (
        'a( )',
        '1()',
        'foo ()',
        ' foo()',
        'foo() ',
        'foo( )',
        'foo(',
        'foo)',
        '()',
        'foo(int a)',
        'foo(int)',
        'foo(int,uint)',
        'foo(int,uint)',
        'foo(int256, uint256)',
        'foo(int256 )',
        'foo( int256)',
    )
)
def test_is_canonical_function_signature_for_invalid_signatures(invalid_signature):
    assert is_canonical_function_signature(invalid_signature) is False
