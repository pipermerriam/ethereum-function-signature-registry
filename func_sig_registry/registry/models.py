from django.db import models
from django.core.validators import MinLengthValidator

from func_sig_registry.utils.github import (
    get_repository_solidity_files,
)
from func_sig_registry.utils.solidity import (
    extract_function_signatures,
    normalize_function_signature,
)
from func_sig_registry.utils.abi import (
    make_4byte_signature,
    function_definition_to_text_signature,
)
from func_sig_registry.utils.encoding import (
    encode_hex,
    force_text,
    force_bytes,
)


class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
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
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if self.bytes_signature_id is None:
            self.bytes_signature, _ = BytesSignature.objects.get_or_create(
                bytes4_signature=force_text(make_4byte_signature(self.text_signature)),
            )
        return super(Signature, self).save()

    #
    # Import methods
    #
    @classmethod
    def import_from_raw_text_signature(cls, raw_function_signature):
        text_signature = normalize_function_signature(raw_function_signature)
        return cls.objects.get_or_create(
            text_signature=text_signature,
        )

    @classmethod
    def import_from_solidity_code(cls, code):
        function_signatures = extract_function_signatures(code)
        return [
            cls.import_from_raw_text_signature(raw_signature)
            for raw_signature in function_signatures
        ]

    @classmethod
    def import_from_solidity_file(cls, file_obj):
        code = force_text(file_obj.read())
        return cls.import_from_solidity_code(code)

    @classmethod
    def import_from_contract_abi(cls, contract_abi):
        function_signatures = [
            function_definition_to_text_signature(function_definition)
            for function_definition in contract_abi
            if function_definition['type'] == 'function'
        ]
        return [
            cls.import_from_raw_text_signature(raw_signature)
            for raw_signature in function_signatures
        ]

    @classmethod
    def import_from_github_repository(cls, username, repository, branch='master'):
        return [
            cls.import_from_solidity_file(file_path)
            for file_path
            in get_repository_solidity_files(username, repository, branch)
        ]


class BytesSignature(models.Model):
    bytes4_signature = models.CharField(max_length=4,
                                        unique=True,
                                        validators=[MinLengthValidator(4)])

    def get_hex_display(self):
        return force_text(encode_hex(force_bytes(self.bytes4_signature)))
