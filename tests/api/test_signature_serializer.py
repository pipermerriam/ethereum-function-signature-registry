import pytest
from func_sig_registry.registry.serializers import SignatureSerializer


def test_serialization(factories):
    signature = factories.SignatureFactory()
    serializer = SignatureSerializer(signature)
    data = serializer.data

    assert data['id'] == signature.id
    assert data['text_signature'] == signature.text_signature
    assert data['bytes_signature'] == signature.bytes_signature.get_hex_display()


@pytest.mark.parametrize(
    'raw_signature,expected',
    (
        ('foo()', 'foo()'),
        (' foo()', 'foo()'),
        ('function foo()', 'foo()'),
        (' function foo()', 'foo()'),
        (' function foo() ', 'foo()'),
    ),
)
def test_creation_with_good_signatures(factories, raw_signature, expected):
    serializer = SignatureSerializer(data={
        'text_signature': raw_signature,
    })
    assert serializer.is_valid(), serializer.errors
    signature = serializer.save()
    assert signature.text_signature == expected


@pytest.mark.parametrize(
    'bad_signature',
    (
        'function()',
        '3()',
    ),
)
def test_creation_with_bad_signatures(factories, bad_signature):
    serializer = SignatureSerializer(data={
        'text_signature': bad_signature,
    })
    assert not serializer.is_valid()
