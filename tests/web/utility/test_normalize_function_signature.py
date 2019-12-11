import pytest

from func_sig_registry.utils.solidity import (
    normalize_function_signature,
)


@pytest.mark.parametrize(
    'raw_signature,expected',
    (
        # from raw signatures
        ('function foo(int a, int b, int c, int d)', 'foo(int256,int256,int256,int256)'),
        ('function foo(address v)', 'foo(address)'),
        ('function   foo  ( address v )', 'foo(address)'),
        ('function foo(address v,\nint i)', 'foo(address,int256)'),
        ('function foo(\naddress   v,\nint i\n)', 'foo(address,int256)'),
        ('function foo (address v)', 'foo(address)'),
        ('function foo(address v, int i)', 'foo(address,int256)'),
        ('function foo(address v,int i)', 'foo(address,int256)'),
        ('function foo(address[] v, int i)', 'foo(address[],int256)'),
        ('function foo(address[2] v, int i)', 'foo(address[2],int256)'),
        ('function foo(address[2][][3] v, int i)', 'foo(address[2][][3],int256)'),
        # without function prefix
        ('foo(int a, int b, int c, int d)', 'foo(int256,int256,int256,int256)'),
        ('foo(address v)', 'foo(address)'),
        ('  foo  ( address v )', 'foo(address)'),
        ('foo(address v,\nint i)', 'foo(address,int256)'),
        ('foo(\naddress   v,\nint i\n)', 'foo(address,int256)'),
        ('foo (address v)', 'foo(address)'),
        ('foo(address v, int i)', 'foo(address,int256)'),
        ('foo(address v,int i)', 'foo(address,int256)'),
        ('foo(address[] v, int i)', 'foo(address[],int256)'),
        ('foo(address[2] v, int i)', 'foo(address[2],int256)'),
        ('foo(address[2][][3] v, int i)', 'foo(address[2][][3],int256)'),
        # poorly normalized
        ('foo(address )', 'foo(address)'),
        ('foo( address)', 'foo(address)'),
        ('foo( address )', 'foo(address)'),
        ('foo (address )', 'foo(address)'),
        ('foo ( address)', 'foo(address)'),
        ('foo ( address )', 'foo(address)'),
        ('foo(int)', 'foo(int256)'),
        ('foo(int,uint)', 'foo(int256,uint256)'),
        ('foo(int, uint)', 'foo(int256,uint256)'),
        ('foo(int, uint )', 'foo(int256,uint256)'),
        ('foo( int, uint)', 'foo(int256,uint256)'),
        ('foo( int, uint )', 'foo(int256,uint256)'),
        (' foo(uint256)', 'foo(uint256)'),
        ('foo(uint256) ', 'foo(uint256)'),
        (' foo(uint256) ', 'foo(uint256)'),
        # bytes32
        ('foo(bytes32)', 'foo(bytes32)'),
        ('foo(address[1])', 'foo(address[1])'),
        ('foo(bytes32[])', 'foo(bytes32[])'),
        ('foo(uint8[])', 'foo(uint8[])'),
        ('foo(uint8[][2][][3])', 'foo(uint8[][2][][3])'),
        ('foo(uint8[][2][][3], uint, bytes32[3][])', 'foo(uint8[][2][][3],uint256,bytes32[3][])'),
        # types in method name
        ('mintToken(uint,address)', 'mintToken(uint256,address)'),
        ('uint()', 'uint()'),
        ('uint256()', 'uint256()'),
        # mixed named/unnamed types
        ('foo(uint x, bool)', 'foo(uint256,bool)'),
        # complex ABI signature
        ('foo(((int,int)[],(bool,fixed))[][2])', 'foo(((int256,int256)[],(bool,fixed128x18))[][2])'),  # noqa: E501
    )
)
def test_normalizing_function_signatures(raw_signature, expected):
    actual = normalize_function_signature(raw_signature)
    assert actual == expected


@pytest.mark.parametrize(
    'raw_signature',
    (
        '0x337b1cf9',
        'foo(T x, U y)',
        'foo(foo x, bar y)',
        # mixed solidity/abi types
        'foo(foo x, (bool,bool) y)',
    )
)
def test_bad_signatures(raw_signature):
    with pytest.raises(ValueError):
        normalize_function_signature(raw_signature)
