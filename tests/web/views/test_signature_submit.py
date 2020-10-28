from func_sig_registry.utils.events_solidity import normalize_event_signature
import pytest

from django.core.urlresolvers import reverse
from django.test import Client
from rest_framework import status

from func_sig_registry.registry.models import (
    Signature,
    EventSignature,
)


@pytest.mark.django_db
def test_function_and_event_signatures_created(api_client):
    create_url = reverse('signature-create')

    text_signature = 'foo(uint a)'
    normalized_text_signature = 'foo(uint256)'

    response = api_client.post(create_url, {'text_signature': text_signature}, follow=True)
    assert(response.status_code == status.HTTP_200_OK)

    function_signatures = Signature.objects.filter(text_signature=normalized_text_signature)
    event_sginatures = EventSignature.objects.filter(text_signature=normalized_text_signature)

    assert(len(function_signatures) == 1)
    assert(len(event_sginatures) == 1)


@pytest.mark.django_db
def test_signatures_created_notification():
    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.post('/submit/', {'text_signature': 'a(uint256)'}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    assert(b'Added function signature a(uint256).' in response.content)
    assert(b'Added event signature a(uint256).' in response.content)


@pytest.mark.django_db
def test_signature_duplicate_notification(factories):
    factories.EventSignatureFactory(text_signature='a(uint256)')
    factories.SignatureFactory(text_signature='a(uint256)')

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)

    response = client.post('/submit/', {'text_signature': 'a(uint256)'}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    assert(b'Function signature a(uint256) already exists.' in response.content)
    assert(b'Event signature a(uint256) already exists.' in response.content)


@pytest.mark.django_db
def test_only_function_siganture_created_notification():
    # Event signature should not be created because signature has too many indexed arguments.
    function = 'foo(uint indexed a, uint indexed b, uint indexed c, uint indexed d, uint indexed e)'
    normalized = 'foo(uint256,uint256,uint256,uint256,uint256)'

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.post('/submit/', {'text_signature': function}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    content = response.content.decode('utf-8')
    assert('Added function signature {0}.'.format(normalized) in content)
    assert('Added event signature {0}'.format(normalized) not in content)


@pytest.mark.django_db
def test_only_event_siganture_created_notification():
    # Function signature should not be created because signature is anonymous.
    signature = 'foo(uint a) anonymous'
    normalized = 'foo(uint256)'

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.post('/submit/', {'text_signature': signature}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    content = response.content.decode('utf-8')
    assert('Added event signature {0}'.format(normalized) in content)
    assert('Added function signature {0}.'.format(normalized) not in content)


@pytest.mark.django_db
def test_error_notification():
    signature = 'foo(List a)'

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.post('/submit/', {'text_signature': signature}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    content = response.content.decode('utf-8')
    assert('Function import error: function args contain non-standard types' in content)
    assert('Event import error: event args contain non-standard types' in content)


@pytest.mark.django_db
def test_specific_error_messages_displayed():
    # Function signature can not be created, because text contains anonynous keyword.
    # Event signature can not be created either, because it has too many indexed arguments.
    signature = 'foo(uint indexed a, uint indexed b, uint indexed c, \
        uint indexed d, uint indexed e) anonymous'

    client = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=True)
    response = client.post('/submit/', {'text_signature': signature}, follow=True)

    assert(response.status_code == status.HTTP_200_OK)
    content = response.content.decode('utf-8')
    assert('Function import error: Could not parse function signature' in content)
    assert('Event import error: Too many indexed arguments' in content)
