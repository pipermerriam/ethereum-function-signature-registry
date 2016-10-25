import json

from rest_framework import serializers

from func_sig_registry.utils.abi import (
    is_valid_contract_abi,
)
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
        source='bytes_signature.get_bytes_display',
        read_only=True,
    )

    class Meta:
        model = Signature
        fields = (
            'id', 'created_at', 'text_signature', 'hex_signature', 'bytes_signature',
        )
        read_only_fields = (
            'created_at', 'hex_signature', 'bytes_signature',
        )

    def validate_text_signature(self, data):
        try:
            signature = normalize_function_signature(data)
        except ValueError:
            raise serializers.ValidationError('Unknown signature format')
        if not is_canonical_function_signature(signature):
            raise serializers.ValidationError('Signature could not be normalized')
        return signature


class SolidityImportSerializer(serializers.Serializer):
    source_file = serializers.FileField(write_only=True, required=False)
    source_code = serializers.CharField(write_only=True, required=False)

    num_processed = serializers.IntegerField(read_only=True)
    num_imported = serializers.IntegerField(read_only=True)
    num_duplicates = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        import_results = []

        if validated_data.get('source_file'):
            import_results.extend(Signature.import_from_solidity_file(
                validated_data['source_file'],
            ))

        if validated_data.get('source_code'):
            import_results.extend(Signature.import_from_solidity_code(
                validated_data['source_code'],
            ))

        num_processed = len(import_results)
        if num_processed == 0:
            num_imported = 0
            num_duplicates = 0
        else:
            num_imported = sum(tuple(zip(*import_results))[1])
            num_duplicates = num_processed - num_imported
        return {
            'num_processed': num_processed,
            'num_imported': num_imported,
            'num_duplicates': num_duplicates,
        }


class ContractABISerializer(serializers.Serializer):
    contract_abi = serializers.CharField(write_only=True)

    num_processed = serializers.IntegerField(read_only=True)
    num_imported = serializers.IntegerField(read_only=True)
    num_duplicates = serializers.IntegerField(read_only=True)

    def validate_contract_abi(self, value):
        try:
            contract_abi = json.loads(value)
        except json.JSONDecodeError:
            raise serializers.ValidationError('Invalid JSON')

        if not is_valid_contract_abi(contract_abi):
            raise serializers.ValidationError('Could not validate ABI')

        return contract_abi

    def create(self, validated_data):
        contract_abi = validated_data['contract_abi']
        import_results = Signature.import_from_contract_abi(contract_abi)
        num_processed = len(import_results)
        if num_processed == 0:
            num_imported = 0
            num_duplicates = 0
        else:
            num_imported = sum(tuple(zip(*import_results))[1])
            num_duplicates = num_processed - num_imported
        return {
            'num_processed': num_processed,
            'num_imported': num_imported,
            'num_duplicates': num_duplicates,
        }


class _OwnerSerializer(serializers.Serializer):
    login = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('login') and not data.get('name'):
            raise serializers.ValidationError("`name` or `login` are required")
        return data


class _RepositorySerializer(serializers.Serializer):
    name = serializers.CharField()
    owner = _OwnerSerializer()


class _HeadCommitSerializer(serializers.Serializer):
    id = serializers.CharField()


class GithubWebhookSerializer(serializers.Serializer):
    repository = _RepositorySerializer()
    head_commit = _HeadCommitSerializer()

    def create(self, validated_data):
        return validated_data
