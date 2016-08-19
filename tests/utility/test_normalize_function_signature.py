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
    )
)
def test_normalizing_function_signatures(raw_signature, expected):
    actual = normalize_function_signature(raw_signature)
    assert actual == expected
