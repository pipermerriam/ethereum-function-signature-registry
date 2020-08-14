import factory

from func_sig_registry.registry.models import (
    Signature,
    BytesSignature,
    EventSignature,
)


class SignatureFactory(factory.DjangoModelFactory):
    text_signature = factory.Sequence(lambda n: "return{n}()".format(n=n))

    class Meta:
        model = Signature


def int_to_bytes4(i):
    unpadded_hex = hex(i)[2:]
    return "0x" + unpadded_hex.zfill(8)


class BytesSignatureFactory(factory.DjangoModelFactory):
    bytes4_signature = factory.Sequence(int_to_bytes4)

    class Meta:
        model = BytesSignature


class EventSignatureFactory(factory.DjangoModelFactory):
    text_signature = factory.Sequence(lambda n: "return{n}()".format(n=n))

    class Meta:
        model = EventSignature
