import rest_framework_filters as filters

from func_sig_registry.utils.encoding import (
    remove_0x_prefix,
)

from .models import (
    EventSignature,
    Signature,
)


class SignatureFilter(filters.FilterSet):
    created_at = filters.AllLookupsFilter(name='created_at')
    text_signature = filters.CharFilter(name='text_signature', lookup_type='icontains')
    bytes_signature = filters.MethodFilter()
    hex_signature = filters.MethodFilter()
    hex_signature__in = filters.MethodFilter()

    class Meta:
        model = Signature
        fields = ['created_at', 'text_signature', 'bytes_signature', 'hex_signature']

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

    def filter_hex_signature__in(self, name, qs, values):
        unprefixed_values = [remove_0x_prefix(value.lower()) for value in values.split(',')]
        return qs.filter(bytes_signature__hex_signature__in=unprefixed_values)


class EventSignatureFilter(filters.FilterSet):
    created_at = filters.AllLookupsFilter(name='created_at')
    text_signature = filters.CharFilter(name='text_signature',
                                        lookup_type='icontains')
    bytes_signature = filters.MethodFilter()
    hex_signature = filters.MethodFilter()

    class Meta:
        model = EventSignature
        fields = ['created_at', 'text_signature',
                  'bytes_signature', 'hex_signature']

    def filter_bytes_signature(self, name, qs, value):
        if len(value) == 32:
            return qs.filter(bytes_signature=value)
        else:
            return qs

    def filter_hex_signature(self, name, qs, value):
        unprefixed_value = remove_0x_prefix(value.lower())

        if len(unprefixed_value) == 64:
            return qs.filter(hex_signature=unprefixed_value)
        else:
            return qs.filter(hex_signature__icontains=unprefixed_value)
