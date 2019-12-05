import pytest

from func_sig_registry.utils.abi import make_4byte_signature


@pytest.mark.parametrize(
    'text_signature,hex_signature',
    (
        ('isCancellable()', '0x4500054f'),
    ),
)
def test_make_4byte_signature(factories, text_signature, hex_signature):
    signature = factories.SignatureFactory(text_signature=text_signature)
    assert hex_signature == signature.bytes_signature.get_hex_display()
