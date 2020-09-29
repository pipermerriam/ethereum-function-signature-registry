import pytest
import string

from django.test import Client

SEARCH_INPUT_WITH_DATA = ' '.join([
    '<input name="bytes4_signature" class="form-control" type="text"',
    'placeholder="0x70a08231" value="0xf0fdf834">',
])
SEARCH_INPUT_EMPTY = ' '.join([
    '<input name="bytes4_signature" class="form-control" type="text"',
    'placeholder="0x70a08231" >',
])

@pytest.mark.django_db
def test_browsable_function_signature_table(factories):
    factories.SignatureFactory(text_signature='a(uint256)')

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.get('/signatures/')

    assert(b'a(uint256)' in response.content)
    assert(b'0xf0fdf834' in response.content)


@pytest.mark.django_db
def test_browsable_function_signature_search(factories):
    factories.SignatureFactory(text_signature='a(uint256)')
    factories.SignatureFactory(text_signature='b(uint256)')

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.get('/signatures/',
                          {'bytes4_signature': '0xf0fdf834'})

    assert(b'a(uint256)' in response.content)
    assert(b'b(uint256)' not in response.content)


@pytest.mark.django_db
def test_function_signature_list_get_context_data():
    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.get('/signatures/',
                          {'bytes4_signature': '0xf0fdf834'})

    assert(str.encode(SEARCH_INPUT_WITH_DATA) in response.content)


@pytest.mark.django_db
def test_function_signature_list_get_context_data_empty():
    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.get('/signatures/')

    print(response.content.decode('utf-8'))

    assert(str.encode(SEARCH_INPUT_EMPTY) in response.content)
