import json

from rest_framework import serializers
from rest_framework.utils import html
from rest_framework.fields import empty

from .models import (
    Signature,
    EventSignature,
)

from func_sig_registry.utils.abi import (
    is_valid_contract_abi,
)

from func_sig_registry.utils.solidity import (
    normalize_function_signature,
)


class SignatureSearchForm(serializers.Serializer):
    bytes4_signature = serializers.CharField(
        style={'placeholder': '0x70a08231'},
    )


class SignatureForm(serializers.ModelSerializer):
    bytes4_signature = serializers.CharField(read_only=True,
                                             source='bytes_signature.get_hex_display')

    class Meta:
        model = Signature
        fields = ('id', 'text_signature', 'bytes4_signature')
        read_only_fields = ('bytes4_signature',)

    def validate_text_signature(self, value):
        return normalize_function_signature(value)


class MultiFileField(serializers.FileField):
    """
    Allow file uploads via inputs with `multipule=true` enabled.
    """
    def __init__(self, *args, **kwargs):
        kwargs['style'] = {'multiple': True, 'template': 'partials/file_input.html'}
        super(MultiFileField, self).__init__(*args, **kwargs)

    def get_value(self, dictionary):
        if self.field_name not in dictionary:
            if getattr(self.root, 'partial', False):
                return empty
        # We override the default field access in order to support
        # lists in HTML forms.
        if html.is_html_input(dictionary):
            val = dictionary.getlist(self.field_name, [])
            if len(val) > 0:
                # Support QueryDict lists in HTML input.
                return val
            return html.parse_html_list(dictionary, prefix=self.field_name)
        return dictionary.getlist(self.field_name, empty)

    def to_internal_value(self, data):
        return data


class SolidityImportForm(serializers.Serializer):
    source_files = MultiFileField()

    def create(self, validated_data):
        return validated_data


class ContractABIForm(serializers.Serializer):
    contract_abi = serializers.CharField(
        style={'base_template': 'textarea.html'},
        write_only=True,
    )

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
        
        #Event Signature handler
        import_results_event = EventSignature.import_from_contract_abi(contract_abi)
        num_processed_event = len(import_results_event)
        if num_processed_event == 0:
            num_imported_event = 0
            num_duplicates_event = 0
        else:
            num_imported_event = sum(tuple(zip(*import_results_event))[1])
            num_duplicates_event = num_processed_event - num_imported_event

        return {
            'num_processed': num_processed + num_processed_event,
            'num_imported': num_imported + num_imported_event,
            'num_duplicates': num_duplicates + num_duplicates_event,
        }
