import pytest

from func_sig_registry.registry.serializers import EventSignatureSerializer
from func_sig_registry.utils.encoding import force_text


def test_serialization(factories):
    signature = factories.EventSignatureFactory()
    serializer = EventSignatureSerializer(signature)
    data = serializer.data

    assert data['id'] == signature.id
    assert data['text_signature'] == signature.text_signature
    assert data['bytes_signature'] == force_text(signature.bytes_signature)
    assert data['hex_signature'] == signature.get_hex_display()


@pytest.mark.parametrize(
    'raw_signature,expected',
    (
        ('foo()', 'foo()'),
        (' foo()', 'foo()'),
        ('event foo()', 'foo()'),
        (' event foo()', 'foo()'),
        (' event foo() ', 'foo()'),
        (' event foo() anonymous ', 'foo()'),
    ),
)
def test_creation_with_good_signatures(factories, raw_signature, expected):
    serializer = EventSignatureSerializer(data={
        'text_signature': raw_signature,
    })
    assert serializer.is_valid(), serializer.errors
    signature = serializer.save()
    assert signature.text_signature == expected


@pytest.mark.parametrize(
    'bad_signature',
    (   
        # reserved word as event name
        'event()',
        # empty text signature
        '',
        # incorrect event name format
        '1asd()',
        # random hex string
        '0x337b1cf9',
        # incorrect type
        'event asd(quint, strong)',
        # too many indexed
        'asd(int indexed, string indexed, address indexed, uint indexed)'
    ),
)
def test_creation_with_bad_signatures(factories, bad_signature):
    serializer = EventSignatureSerializer(data={
        'text_signature': bad_signature,
    })
    assert not serializer.is_valid()
