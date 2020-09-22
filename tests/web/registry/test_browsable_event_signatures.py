import pytest
import string

from django.test import Client

EVENT_SIGNATURE_HTML = '<td class="text_signature">a(uint256)</td>'
EVENT_SIGNATURE_HEX_HTML = ''.join([
    '<td class="hex_signature">',
    '<code>',
    '0xf0fdf83467af68171df09204c0b00056c1e4c80e368b3fff732778b858f7966d',
    '</code>',
    '</td>',
])


@pytest.mark.django_db
def test_browsable_event_signature_html(factories):
    factories.EventSignatureFactory(text_signature='a(uint256)')

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.get('/event-signatures/')

    assert(str.encode(EVENT_SIGNATURE_HTML) in response.content)
    assert(str.encode(EVENT_SIGNATURE_HEX_HTML) in response.content)


@pytest.mark.django_db
def test_browsable_event_signature_search(factories):
    factories.EventSignatureFactory(text_signature='a(uint256)')
    factories.EventSignatureFactory(text_signature='b(uint256)')

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    # requesting prefix
    response = client.get('/event-signatures/', {'bytes_signature': '0xf0fdf83467af68171df09204c0'})

    assert(b'a(uint256)' in response.content)
    assert(b'b(uint256)' not in response.content)
