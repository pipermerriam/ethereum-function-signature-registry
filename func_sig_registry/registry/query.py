from django.db import models

from func_sig_registry.utils.encoding import (
    decode_hex,
)


class PersonQuerySet(models.QuerySet):
    def search_bytes4_signature(self, hex_query):
        bytes_query = decode_hex(hex_query)
        return self.filter(bytes_signature__bytes4_signature__icontains=bytes_query)
