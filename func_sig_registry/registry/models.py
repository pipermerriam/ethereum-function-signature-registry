import logging
import sys

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from django.core.exceptions import ValidationError
from eth_utils import event_signature_to_log_topic

from func_sig_registry.utils.github import (
    get_repository_solidity_files,
)
from func_sig_registry.utils.solidity import (
    extract_function_signatures,
    normalize_function_signature,
)
from func_sig_registry.utils.events_solidity import (
    normalize_event_signature,
    extract_event_signatures,
)
from func_sig_registry.utils.abi import (
    make_4byte_signature,
    function_definition_to_text_signature,
    event_definition_to_text_signature,
)
from func_sig_registry.utils.encoding import (
    encode_hex,
    force_text,
    add_0x_prefix,
    remove_0x_prefix,
)


logger = logging.getLogger('bytes4.models')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Signature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    text_signature = models.TextField(unique=True,
                                      validators=[
                                          MinLengthValidator(3),
                                      ])
    bytes_signature = models.ForeignKey(
        'registry.BytesSignature',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.text_signature

    def clean_fields(self, exclude=None):
        try:
            self.text_signature = normalize_function_signature(self.text_signature)
        except ValueError:
            raise ValidationError('Unknown signature format')

    class Meta:
        unique_together = (
            ('text_signature', 'bytes_signature'),
        )
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if self.bytes_signature_id is None:
            bytes4_signature = make_4byte_signature(self.text_signature)
            hex_signature = force_text(remove_0x_prefix(encode_hex(bytes4_signature)))
            self.bytes_signature, _ = BytesSignature.objects.get_or_create(
                bytes4_signature=bytes4_signature,
                defaults={'hex_signature': hex_signature},
            )
        return super(Signature, self).save()

    #
    # Import methods
    #
    @classmethod
    def import_from_raw_text_signature(cls, raw_function_signature):
        try:
            text_signature = normalize_function_signature(raw_function_signature)
        except ValueError:
            logger.error("error signature: %s", raw_function_signature)
        else:
            logger.info("importing signature: %s", text_signature)
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
    def import_from_github_repository(cls, login_or_name, repository, branch='master'):
        for file_path in get_repository_solidity_files(login_or_name, repository, branch):
            logger.info("importing solidity file: %s", file_path)
            with open(file_path) as solidity_file:
                try:
                    cls.import_from_solidity_file(solidity_file)
                except UnicodeDecodeError:
                    logger.error('unicode error reading solidity file: %s', file_path)


class BytesSignature(models.Model):
    bytes4_signature = models.BinaryField(max_length=4,
                                          unique=True,
                                          validators=[MinLengthValidator(4)])
    hex_signature = models.CharField(max_length=8,
                                     unique=True,
                                     validators=[MinLengthValidator(8)])

    def save(self, *args, **kwargs):
        if not self.hex_signature:
            self.hex_signature = force_text(remove_0x_prefix(encode_hex(self.bytes4_signature)))
        super(BytesSignature, self).save(*args, **kwargs)

    def get_hex_display(self):
        return force_text(add_0x_prefix(self.hex_signature))

    def get_bytes_display(self):
        return force_text(self.bytes4_signature)


class EventSignature(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    text_signature = models.TextField(unique=True,
                                        validators=[
                                            MinLengthValidator(3), MaxLengthValidator(4096)
                                        ])

    bytes_signature = models.BinaryField(max_length=32,
                                            unique=True,
                                            validators=[MinLengthValidator(32)])
                                          
    hex_signature = models.CharField(max_length=64,
                                        unique=True,
                                        validators=[MinLengthValidator(64)])

    def __str__(self):
        return self.text_signature

    def clean_fields(self, exclude=None):
        try:
            #TODO
            self.text_signature = normalize_event_signature(self.text_signature)
        except ValueError:
            raise ValidationError('Unknown signature format')

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if len(self.bytes_signature) == 0 or len(self.hex_signature) == 0:
            self.bytes_signature = event_signature_to_log_topic(self.text_signature)
            self.hex_signature = force_text(remove_0x_prefix(encode_hex(self.bytes_signature)))
        return super(EventSignature, self).save()

    def get_hex_display(self):
        return force_text(add_0x_prefix(self.hex_signature))

    def get_bytes_display(self):
        return force_text(self.bytes_signature)

    #
    # Import methods
    #
    @classmethod
    def import_from_raw_text_signature(cls, raw_event_signature):
        try:
            text_signature = normalize_event_signature(raw_event_signature)
        except ValueError:
            logger.error("error signature: %s", raw_event_signature)
        else:
            logger.info("importing signature: %s", text_signature)
            return cls.objects.get_or_create(
                text_signature=text_signature,
            )

    @classmethod
    def import_from_solidity_code(cls, code):
        event_signatures = extract_event_signatures(code)
        return [
            cls.import_from_raw_text_signature(raw_signature)
            for raw_signature in event_signatures
        ]

    @classmethod
    def import_from_solidity_file(cls, file_obj):
        code = force_text(file_obj.read())
        return cls.import_from_solidity_code(code)

    @classmethod
    def import_from_contract_abi(cls, contract_abi):
        event_signatures = [
            event_definition_to_text_signature(event_definition)
            for event_definition in contract_abi
            if event_definition['type'] == 'event'
        ]
        return [
            cls.import_from_raw_text_signature(raw_signature)
            for raw_signature in event_signatures
        ]

    @classmethod
    def import_from_github_repository(cls, login_or_name, repository, branch='master'):
        for file_path in get_repository_solidity_files(login_or_name, repository, branch):
            logger.info("importing solidity file: %s", file_path)
            with open(file_path) as solidity_file:
                try:
                    cls.import_from_solidity_file(solidity_file)
                except UnicodeDecodeError:
                    logger.error('unicode error reading solidity file: %s', file_path)
