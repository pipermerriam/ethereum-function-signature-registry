from rest_framework import serializers

from .models import Signature

from .utils import (
    clean_text_signature,
)


class SignatureSearchSerializer(serializers.Serializer):
    bytes4_signature = serializers.CharField()


class SignatureSerializer(serializers.ModelSerializer):
    bytes4_signature = serializers.CharField(read_only=True,
                                             source='bytes_signature.get_hex_display')

    class Meta:
        model = Signature
        fields = ('id', 'text_signature', 'bytes4_signature')
        read_only_fields = ('bytes4_signature',)

    def validate_signature(self, value):
        return clean_text_signature(value)


class SolidityImportSerializer(serializers.Serializer):
    source_file = serializers.FileField()

    def create(self, validated_data):
        return validated_data['source_file']
