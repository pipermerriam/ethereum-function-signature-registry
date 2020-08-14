import pytest

from func_sig_registry.utils.events_solidity import (
    normalize_event_signature
)


@pytest.mark.parametrize(
    'raw_signature,expected',
    (
        # from raw signatures
        ('event foo(int a, int b, int c, int d)', 'foo(int256,int256,int256,int256)'),
        ('event foo(address v)', 'foo(address)'),
        ('event   foo  ( address v )', 'foo(address)'),
        ('event foo(address v,\nint i)', 'foo(address,int256)'),
        ('event foo(\naddress   v,\nint i\n)', 'foo(address,int256)'),
        ('event foo (address v)', 'foo(address)'),
        ('event foo(address v, int i)', 'foo(address,int256)'),
        ('event foo(address v,int i)', 'foo(address,int256)'),
        ('event foo(address[] v, int i)', 'foo(address[],int256)'),
        ('event foo(address[2] v, int i)', 'foo(address[2],int256)'),
        ('event foo(address[2][][3] v, int i)', 'foo(address[2][][3],int256)'),
        # without event prefix
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
        # indexed Arguments
        ('foo(uint indexed a, string indexed b, address indexed c)', 'foo(uint256,string,address)'),
        ('foo(uint indexed a)', 'foo(uint256)'),
        # anonymous keyword
        ('foo(uint) anonymous ', 'foo(uint256)')
    )
)
def test_normalizing_event_signatures(raw_signature, expected):
    actual = normalize_event_signature(raw_signature)
    assert actual == expected


@pytest.mark.parametrize(
    'raw_signature',
    (
        '0x337b1cf9',
        'foo(T x, U y)',
        'foo(foo x, bar y)',
        # mixed solidity/abi types
        'foo(foo x, (bool,bool) y)',
        # too many indexed arguments
        'foo(uint indexed a, string indexed b, address indexed c, int indexed d)',
        'foo(uint indexed a, string indexed b, address indexed c, int indexed d, string indexed e)',
        # event name
        'event 2asd(uint)',
        'qwe qwe(uint)',
        # random
        'anonymous asd(uint) anonymous'
    )
)
def test_bad_event_signatures(raw_signature):
    with pytest.raises(ValueError):
        normalize_event_signature(raw_signature)
