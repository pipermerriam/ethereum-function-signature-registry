import rest_framework_filters as filters

from func_sig_registry.utils.encoding import (
    decode_hex,
    force_bytes,
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
        if len(value) > 4:
            # invalid length
            return qs
        elif len(value) == 4:
            return qs.filter(bytes_signature__bytes4_signature=force_bytes(value))
        else:
            return qs.filter(bytes_signature__bytes4_signature__icontains=force_bytes(value))

    def filter_hex_signature(self, name, qs, value):
        try:
            bytes_value = decode_hex(value)
        except Exception:
            return qs
        else:
            return self.filter_bytes_signature(name, qs, bytes_value)
