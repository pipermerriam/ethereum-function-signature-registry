import rest_framework_filters as filters

from func_sig_registry.utils.encoding import (
    remove_0x_prefix,
)

from .models import Signature


class SignatureFilter(filters.FilterSet):
    text_signature = filters.CharFilter(name='text_signature', lookup_type='icontains')
    bytes_signature = filters.MethodFilter()
    hex_signature = filters.MethodFilter()

    class Meta:
        model = Signature
        fields = ['text_signature', 'bytes_signature', 'hex_signature']

    def filter_bytes_signature(self, name, qs, value):
        if len(value) == 4:
            return qs.filter(bytes_signature__bytes4_signature=value)
        else:
            return qs

    def filter_hex_signature(self, name, qs, value):
        unprefixed_value = remove_0x_prefix(value.lower())

        if len(unprefixed_value) == 8:
            return qs.filter(bytes_signature__hex_signature=unprefixed_value)
        else:
            return qs.filter(bytes_signature__hex_signature__icontains=unprefixed_value)
