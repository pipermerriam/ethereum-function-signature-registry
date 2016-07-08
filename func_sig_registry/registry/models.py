from django.db import models
from django.core.validators import MinLengthValidator

from .parsers import (
    extract_function_signatures,
    normalize_function_signature,
)
from .utils import (
    make_4byte_signature,
    encode_hex,
    force_text,
    force_bytes,
)


class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    text_signature = models.TextField(unique=True,
                                      validators=[
                                          MinLengthValidator(3),
                                      ])
    bytes_signature = models.ForeignKey('registry.BytesSignature')

    class Meta:
        unique_together = (
            ('text_signature', 'bytes_signature'),
        )

    def save(self, *args, **kwargs):
        if self.bytes_signature_id is None:
            self.bytes_signature, _ = BytesSignature.objects.get_or_create(
                bytes4_signature=force_text(make_4byte_signature(self.text_signature)),
            )
        super(Signature, self).save()

    @classmethod
    def import_from_solidity_source(cls, file_obj):
        source_code = force_text(file_obj.read())
        raw_function_signatures = extract_function_signatures(source_code)
        function_signatures = (
            normalize_function_signature(sig) for sig in raw_function_signatures
        )
        for text_signature in function_signatures:
            Signature.objects.get_or_create(text_signature=text_signature)


class BytesSignature(models.Model):
    bytes4_signature = models.CharField(max_length=4,
                                        unique=True,
                                        validators=[MinLengthValidator(4)])

    def get_hex_display(self):
        return force_text(encode_hex(force_bytes(self.bytes4_signature)))
