from web3.utils.string import (
    force_text,
    force_bytes,
)

from func_sig_registry.utils.signature_db import (
    function_definition_to_kwargs,
)
from func_sig_registry.utils.abi import (
    make_4byte_signature,
    function_definition_to_text_signature,
)


ABI_A = {
    'name': 'foo',
    'inputs': [],
    'type': 'function',
}
ABI_A_SIGNATURE = function_definition_to_text_signature(ABI_A)
ABI_A_SELECTOR_BYTES = make_4byte_signature(ABI_A_SIGNATURE)
ABI_A_SELECTOR = force_text(ABI_A_SELECTOR_BYTES)


def test_adding_signature_to_db(chain, signature_db):
    assert signature_db.call().isKnownSelector(ABI_A_SELECTOR_BYTES) is False
    assert signature_db.call().isKnownSignature(ABI_A_SIGNATURE) is False

    create_kwargs = function_definition_to_kwargs(ABI_A)
    chain.wait.for_receipt(signature_db.transact().addSignature(**create_kwargs))

    assert signature_db.call().isKnownSelector(ABI_A_SELECTOR_BYTES) is True
    assert signature_db.call().isKnownSignature(ABI_A_SIGNATURE) is True

    assert signature_db.call().numSignatures(ABI_A_SELECTOR_BYTES) == 1

    signature_hash = signature_db.call().getSignatureHash(ABI_A_SELECTOR_BYTES, 0)
    signature_hash_bytes = force_bytes(signature_hash)

    assert signature_hash_bytes.startswith(ABI_A_SELECTOR_BYTES)

    signature = signature_db.call().getSignature(signature_hash_bytes)

    assert signature == ABI_A_SIGNATURE
    assert signature_db.call().getSignature(ABI_A_SELECTOR_BYTES, 0) == signature

    assert signature_db.call().getAllSignatureHashes(ABI_A_SELECTOR_BYTES) == [signature_hash]


COLLISION_ABI_A = {
    'name': 'SkillBeatsLuck',
    'inputs': [],
    'type': 'function',
}
COLLISION_A_SIGNATURE = function_definition_to_text_signature(COLLISION_ABI_A)
COLLISION_A_SELECTOR_BYTES = make_4byte_signature(COLLISION_A_SIGNATURE)
COLLISION_A_SELECTOR = force_text(COLLISION_A_SELECTOR_BYTES)


COLLISION_ABI_B = {
    'name': '_594078427145613',
    'inputs': [],
    'type': 'function',
}
COLLISION_B_SIGNATURE = function_definition_to_text_signature(COLLISION_ABI_B)
COLLISION_B_SELECTOR_BYTES = make_4byte_signature(COLLISION_B_SIGNATURE)
COLLISION_B_SELECTOR = force_text(COLLISION_B_SELECTOR_BYTES)

assert COLLISION_A_SELECTOR == COLLISION_B_SELECTOR


def test_selector_collision(chain, signature_db):
    assert signature_db.call().isKnownSelector(COLLISION_A_SELECTOR_BYTES) is False
    assert signature_db.call().isKnownSignature(COLLISION_A_SIGNATURE) is False
    create_a_kwargs = function_definition_to_kwargs(COLLISION_ABI_A)
    chain.wait.for_receipt(signature_db.transact().addSignature(**create_a_kwargs))
    assert signature_db.call().isKnownSelector(COLLISION_A_SELECTOR_BYTES) is True
    assert signature_db.call().isKnownSignature(COLLISION_A_SIGNATURE) is True

    assert signature_db.call().isKnownSelector(COLLISION_B_SELECTOR_BYTES) is True
    assert signature_db.call().isKnownSignature(COLLISION_B_SIGNATURE) is False
    create_b_kwargs = function_definition_to_kwargs(COLLISION_ABI_B)
    chain.wait.for_receipt(signature_db.transact().addSignature(**create_b_kwargs))
    assert signature_db.call().isKnownSelector(COLLISION_B_SELECTOR_BYTES) is True
    assert signature_db.call().isKnownSignature(COLLISION_B_SIGNATURE) is True

    assert signature_db.call().numSignatures(COLLISION_A_SELECTOR_BYTES) == 2
