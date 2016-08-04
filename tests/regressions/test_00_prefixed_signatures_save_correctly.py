import pytest

from func_sig_registry.utils.encoding import (
    force_text,
)
from func_sig_registry.utils.abi import (
    make_4byte_signature,
)


@pytest.mark.parametrize(
    'text_signature,bytes4_signature',
    (
        ('NewPoll(string,string,uint256,uint256)', '\x00\x10\n\x18'),
        ('computeResponse(uint256,uint16)', '\x00µ²#'),
        ('setLowerFeePercentage(uint8)', '\x00;\x9d\x88'),
        ('setHand(uint256)', '\x00Ç!«'),
        ('comparisonchr(string)', '\x00\x873g'),
        ('getTokenDivisor()', '\x00úôÝ'),
        ('getFrontend()', '\x000tÿ'),
        ('triggerPayment()', '\x00Î W'),
        ('setMinimumPassPercentage(uint8)', '\x00äg\x00'),
    ),
)
def test_00_prefixed_signatures_result_in_correct_4byte_signature(factories,
                                                                  models,
                                                                  text_signature,
                                                                  bytes4_signature):
    signature = models.Signature(text_signature=text_signature)
    signature.save()

    bytes_signature = models.BytesSignature.objects.get(pk=signature.bytes_signature_id)

    assert len(bytes_signature.bytes4_signature) == 4
    assert bytes_signature.get_bytes_display() == bytes4_signature
