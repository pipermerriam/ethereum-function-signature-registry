import datetime
import pytest

from rest_framework import status
from django.core.urlresolvers import reverse
from django.utils import timezone

from eth_utils import event_signature_to_log_topic

from func_sig_registry.utils.encoding import force_text
from func_sig_registry.utils.events_solidity import normalize_event_signature

EVENT_API_URL = '/api/v1/event-signatures/'


def test_event_signature_api_count(api_client, factories):
    factories.EventSignatureFactory.create_batch(35)

    response = api_client.get(EVENT_API_URL)

    assert response.status_code == status.HTTP_200_OK
    count = response.data['count']

    assert count == 35


def test_event_signature_api_pagination(api_client, factories):
    factories.EventSignatureFactory.create_batch(101)

    response = api_client.get(EVENT_API_URL)

    assert response.status_code == status.HTTP_200_OK
    data = response.data

    assert len(data['results']) == 100


def test_event_signature_api_ordering(api_client, factories):
    ascending_url = EVENT_API_URL + "?ordering=created_at"
    decending_url = EVENT_API_URL + "?ordering=-created_at"

    factories.EventSignatureFactory()

    sig_b = factories.EventSignatureFactory()
    sig_b.created_at = timezone.now() + datetime.timedelta(1)

    response_a = api_client.get(ascending_url)
    assert response_a.status_code == status.HTTP_200_OK
    results_a = response_a.data['results']

    response_b = api_client.get(decending_url)
    assert response_b.status_code == status.HTTP_200_OK
    results_b = response_b.data['results']

    assert len(results_a) == 2
    assert len(results_b) == 2
    assert tuple(v['id'] for v in results_a) == tuple(reversed(tuple(v['id'] for v in results_b)))


def test_event_signature_api_pagination_page_size_query_param(api_client, factories):
    list_url = EVENT_API_URL + '?page_size=50'
    factories.EventSignatureFactory.create_batch(101)

    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 101
    assert len(data['results']) == 50


def test_event_signature_api_create(api_client):
    response = api_client.post(EVENT_API_URL,
                               {'text_signature': 'account(address)'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['text_signature'] == 'account(address)'
    assert data['bytes_signature'] == force_text(
        event_signature_to_log_topic(data['text_signature']))
    assert data['hex_signature'] == '0x73b9aa91e3748e9df0e79073dca453a3ec1c019407cb9290c3173ad56df0f573'


def test_create_duplicate_signature(api_client, factories):
    signature = factories.EventSignatureFactory()

    response = api_client.post(EVENT_API_URL,
                               {'text_signature': signature.text_signature})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_complex_signature(api_client):
    text_signature = 'getOrdersInfo((address,address,address,address,uint256,uint256,uint256,uint256,uint256,uint256,bytes,bytes)[])'  # noqa: E501

    response = api_client.post(EVENT_API_URL,
                               {'text_signature': text_signature})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['text_signature'] == text_signature
    assert data['bytes_signature'] == force_text(
        event_signature_to_log_topic(
            normalize_event_signature(data['text_signature'])))
    assert data['hex_signature'] == '0x7e9d74dc5e5d1a841950b2603b1fc48e0a1c1391bbb4ed24915c26cf1ff33ccb'


def test_retrieve_signature(api_client, factories):
    signature = factories.EventSignatureFactory()
    detail_url = EVENT_API_URL + str(signature.id) + '/'

    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    data = response.data

    assert data['id'] == signature.id
    assert data['text_signature'] == signature.text_signature
    assert data['bytes_signature'] == force_text(signature.bytes_signature)
    assert data['hex_signature'] == signature.get_hex_display()


def test_cannot_update_with_put_signature(api_client, factories):
    signature = factories.EventSignatureFactory()
    detail_url = EVENT_API_URL + str(signature.id) + '/'

    response = api_client.put(detail_url, {'text_signature': 'newEvent()'})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_cannot_update_with_post_signature(api_client, factories):
    signature = factories.EventSignatureFactory()
    detail_url = EVENT_API_URL + str(signature.id) + '/'

    response = api_client.post(detail_url, {'text_signature': 'newFunction()'})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_cannot_delete_signature(api_client, factories):
    signature = factories.EventSignatureFactory()
    detail_url = EVENT_API_URL + str(signature.id) + '/'

    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_exact_hex_search(api_client, factories):
    s1, s2, s3, s4, s5 = factories.EventSignatureFactory.create_batch(5)

    search_url = EVENT_API_URL + '?hex_signature={0}'.format(
        s2.get_hex_display())
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_exact_without_0x_hex_search(api_client, factories):
    s1, s2, s3, s4, s5 = factories.EventSignatureFactory.create_batch(5)

    search_url = EVENT_API_URL + '?hex_signature={0}'.format(
        s2.get_hex_display()[2:])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_substring_hex_search_with_0x(api_client, factories):
    s1, s2, s3, s4, s5 = factories.EventSignatureFactory.create_batch(5)

    search_url = EVENT_API_URL + '?hex_signature={0}'.format(
        s2.get_hex_display()[:8])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_substring_hex_search_without_0x(api_client, factories):
    s1, s2, s3, s4, s5 = factories.EventSignatureFactory.create_batch(5)

    search_url = EVENT_API_URL + '?hex_signature={0}'.format(
        s2.get_hex_display()[2:8])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id
