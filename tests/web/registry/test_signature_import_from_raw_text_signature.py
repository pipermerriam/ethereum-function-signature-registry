import pytest


@pytest.mark.parametrize(
    'raw_signature,expected',
    (
        ('balanceOf(address who)', 'balanceOf(address)'),
        ('balanceOf( address who )', 'balanceOf(address)'),
        ('balanceOf( address who )', 'balanceOf(address)'),
        ('transfer(address who, uint amount)', 'transfer(address,uint256)'),
        ('register(bytes32[] names, uint[] values)', 'register(bytes32[],uint256[])'),
    )
)
def test_import_from_raw_text_signature(raw_signature, expected, models):
    sig, _ = models.Signature.import_from_raw_text_signature(raw_signature)
    assert sig.text_signature == expected


@pytest.mark.parametrize(
    'bad_signature',
    (
        'balanceOf(',
        '0x1234abcd',
        '[]',
    )
)
def test_import_from_raw_text_signature_with_bad_signatures(bad_signature, models):
    with pytest.raises(ValueError):
        models.Signature.import_from_raw_text_signature(bad_signature)
