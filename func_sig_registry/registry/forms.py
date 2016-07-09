from rest_framework import serializers
from rest_framework.utils import html
from rest_framework.fields import empty

from .models import Signature

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

    def validate_signature(self, value):
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
