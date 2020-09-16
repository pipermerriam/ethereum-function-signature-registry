import json

from rest_framework import serializers
from rest_framework.utils import html
from rest_framework.fields import empty

from .models import (
    Signature,
    EventSignature,
)

from func_sig_registry.utils.import_statistics import (
    retrieve_stats_from_import_results,
)

from func_sig_registry.utils.abi import (
    is_valid_contract_abi,
)

from func_sig_registry.utils.solidity import (
    normalize_function_signature,
)

from func_sig_registry.utils.events_solidity import (
    normalize_event_signature,
)


class SignatureSearchForm(serializers.Serializer):
    bytes4_signature = serializers.CharField(
        style={'placeholder': '0x70a08231'},
    )


class EventSignatureSearchForm(serializers.Serializer):
    bytes_signature = serializers.CharField(
        style={'placeholder': '0x82ff462f689e2f73df9fd8306282ad3ad112aca9e0847911e8051e158c525b33'},
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


class AllSignatureCreateForm(serializers.Serializer):
    text_signature = serializers.CharField(write_only=True)

    def create(self, validated_data):
        message_parts = []
        if 'function_signature' in validated_data['text_signature']:
            function_signature_tuple = Signature.import_from_raw_text_signature(
                validated_data['text_signature']['function_signature'],
                )
            function_signature = function_signature_tuple[0]
            message_parts.append('Added function signature {0} for function {1}.'.format(
                function_signature.bytes_signature.get_hex_display(),
                function_signature.text_signature,
            ))
        if 'event_signature' in validated_data['text_signature']:
            event_signature_tuple = EventSignature.import_from_raw_text_signature(
                validated_data['text_signature']['event_signature'],
            )
            event_signature = event_signature_tuple[0]
            message_parts.append('Added event signature {0} for event {1}.'.format(
                event_signature.get_hex_display(),
                event_signature.text_signature,
            ))
        return {
            'response_message': ' '.join(message_parts),
            }

    def validate_text_signature(self, value):
        validated_signatures = dict()
        try:
            normalized_function_signature = normalize_function_signature(value)
            validated_signatures.update({'function_signature' : normalized_function_signature})
        except:
            pass

        try:
            normalized_event_signature = normalize_event_signature(value)
            validated_signatures.update({'event_signature' : normalized_event_signature})
        except:
            pass

        if len(validated_signatures) == 0:
            raise ValueError('Could not parse given signature')
        return validated_signatures



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
    num_ignored = serializers.IntegerField(read_only=True)

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

        stats_function = retrieve_stats_from_import_results(
            Signature.import_from_contract_abi(contract_abi))
        stats_event = retrieve_stats_from_import_results(
            EventSignature.import_from_contract_abi(contract_abi))

        return {
            'num_processed':
                stats_function.num_processed + stats_event.num_processed,
            'num_imported':
                stats_function.num_imported + stats_event.num_imported,
            'num_duplicates':
                stats_function.num_duplicates + stats_event.num_duplicates,
            'num_ignored':
                stats_function.num_ignored + stats_event.num_ignored,
        }
