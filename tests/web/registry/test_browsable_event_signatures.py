import pytest
import string

from django.test import Client

EVENT_TEXT_SIGNATURE = 'a(uint256)'
EVENT_HEX_SIGNATURE = '0xf0fdf83467af68171df09204c0b00056c1e4c80e368b3fff732778b858f7966d'

EVENT_SIGNATURE_HTML = f'<td class="text_signature">{EVENT_TEXT_SIGNATURE}</td>'
EVENT_SIGNATURE_HEX_HTML = ''.join([
    '<td class="hex_signature">',
    '<code>',
    EVENT_HEX_SIGNATURE,
    '</code>',
    '</td>',
])

SEARCH_INPUT_HTML_WITH_VALUE = ' '.join([
    '<input name="bytes_signature" class="form-control" type="text"',
    'placeholder="0x82ff462f689e2f73df9fd8306282ad3ad112aca9e0847911e8051e158c525b33"',
    f'value="{EVENT_HEX_SIGNATURE}">',
])
SEARCH_INPUT_HTML_EMPTY = ' '.join([
    '<input name="bytes_signature" class="form-control" type="text"',
    'placeholder="0x82ff462f689e2f73df9fd8306282ad3ad112aca9e0847911e8051e158c525b33" >'
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

    response = client.get('/event-signatures/',
                          {'bytes_signature': EVENT_HEX_SIGNATURE})

    assert(b'a(uint256)' in response.content)
    assert(b'b(uint256)' not in response.content)


@pytest.mark.django_db
def test_event_signature_list_get_context_data():
    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.get('/event-signatures/',
                          {'bytes_signature': EVENT_HEX_SIGNATURE})

    assert(str.encode(SEARCH_INPUT_HTML_WITH_VALUE) in response.content)


@pytest.mark.django_db
def test_event_signature_list_get_context_data_empty():
    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.get('/event-signatures/')

    assert(str.encode(SEARCH_INPUT_HTML_EMPTY) in response.content)
