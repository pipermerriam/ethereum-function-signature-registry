from django.core.exceptions import ValidationError

from func_sig_registry.utils.solidity import (
    is_raw_function_signature,
    is_canonical_function_signature,
)


def validate_raw_function_signature(signature):
    if not is_raw_function_signature(signature):
        raise ValidationError('Invalid function signature')


def validate_canonical_function_signature(signature):
    if not is_canonical_function_signature(signature):
        raise ValidationError('Invalid function signature')
