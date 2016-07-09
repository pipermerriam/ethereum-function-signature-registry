from rest_framework import serializers

from func_sig_registry.utils.solidity import (
    normalize_function_signature,
    is_canonical_function_signature,
)

from .models import Signature


class SignatureSerializer(serializers.ModelSerializer):
    hex_signature = serializers.CharField(
        source='bytes_signature.get_hex_display',
        read_only=True,
    )
    bytes_signature = serializers.CharField(
        source='bytes_signature.bytes4_signature',
        read_only=True,
    )

    class Meta:
        model = Signature
        fields = (
            'id', 'text_signature', 'hex_signature', 'bytes_signature',
        )
        read_only_fields = (
            'hex_signature', 'bytes_signature',
        )

    def validate_text_signature(self, data):
        try:
            signature = normalize_function_signature(data)
        except ValueError:
            raise serializers.ValidationError('Unknown signature format')
        if not is_canonical_function_signature(signature):
            raise serializers.ValidationError('Signature could not be normalized')
        return signature
