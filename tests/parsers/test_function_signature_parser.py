import pytest

from func_sig_registry.registry.parsers import (
    extract_function_signatures,
    normalize_function_signature,
)


@pytest.mark.parametrize(
    'code',
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
def test_function_signature_extraction(code):
    raw_signatures = extract_function_signatures(code)
    print(raw_signatures)
    assert len(raw_signatures) == 1


@pytest.mark.parametrize(
    'raw_signature,normalized_signature',
    (
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
    )
)
def test_normalizing_function_signatures(raw_signature, normalized_signature):
    actual = normalize_function_signature(raw_signature)
    assert actual == normalized_signature
