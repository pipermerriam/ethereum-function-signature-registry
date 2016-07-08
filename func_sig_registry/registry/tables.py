import django_tables2 as tables

from .models import (
    Signature,
)


class SignatureTable(tables.Table):
    bytes_signature = tables.TemplateColumn(
        '<code>{{ record.bytes_signature.get_hex_display }}</code>',
    )

    class Meta:
        model = Signature
        fields = (
            'id',
            'text_signature',
            'bytes_signature',
        )
        template = 'partials/table.html'
        attrs = {
            'class': 'table table-striped table-bordered',
        }
