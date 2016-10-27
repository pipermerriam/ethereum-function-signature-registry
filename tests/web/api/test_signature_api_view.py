import datetime

from rest_framework import status

from django.core.urlresolvers import reverse
from django.utils import timezone

from func_sig_registry.utils.encoding import (
    force_text,
)


def test_list_view(api_client, factories):
    list_url = reverse('api:signature-list')
    factories.SignatureFactory.create_batch(5)

    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 5
    assert len(data['results']) == 5


def test_list_view_pagination(api_client, factories):
    list_url = reverse('api:signature-list')
    factories.SignatureFactory.create_batch(101)

    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 101
    assert len(data['results']) == 100


def test_list_view_ordering(api_client, factories):
    list_url = reverse('api:signature-list')

    ascending_url = list_url + "?ordering=created_at"
    decending_url = list_url + "?ordering=-created_at"

    factories.SignatureFactory()

    sig_b = factories.SignatureFactory()
    sig_b.created_at = timezone.now() + datetime.timedelta(1)

    response_a = api_client.get(ascending_url)
    assert response_a.status_code == status.HTTP_200_OK
    results_a = response_a.data['results']

    response_b = api_client.get(decending_url)
    assert response_b.status_code == status.HTTP_200_OK
    results_b = response_b.data['results']

    assert tuple(v['id'] for v in results_a) == tuple(reversed(tuple(v['id'] for v in results_b)))


def test_list_view_pagination_page_size_query_param(api_client, factories):
    list_url = reverse('api:signature-list') + '?page_size=50'
    factories.SignatureFactory.create_batch(101)

    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 101
    assert len(data['results']) == 50


def test_create_signature(api_client):
    create_url = reverse('api:signature-list')

    response = api_client.post(create_url, {'text_signature': 'balanceOf(address)'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['text_signature'] == 'balanceOf(address)'
    assert data['bytes_signature'] == 'p\xa0\x821'
    assert data['hex_signature'] == '0x70a08231'


def test_create_duplicate_signature(api_client, factories):
    create_url = reverse('api:signature-list')
    signature = factories.SignatureFactory()

    response = api_client.post(create_url, {'text_signature': signature.text_signature})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_signature(api_client, factories):
    signature = factories.SignatureFactory()
    detail_url = reverse('api:signature-detail', kwargs={'pk': signature.pk})

    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK

    data = response.data

    assert data['id'] == signature.id
    assert data['text_signature'] == signature.text_signature
    assert data['bytes_signature'] == force_text(signature.bytes_signature.bytes4_signature)
    assert data['hex_signature'] == signature.bytes_signature.get_hex_display()


def test_cannot_update_with_put_signature(api_client, factories):
    signature = factories.SignatureFactory()
    detail_url = reverse('api:signature-detail', kwargs={'pk': signature.pk})

    response = api_client.put(detail_url, {'text_signature': 'newFunction()'})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_cannot_update_with_post_signature(api_client, factories):
    signature = factories.SignatureFactory()
    detail_url = reverse('api:signature-detail', kwargs={'pk': signature.pk})

    response = api_client.post(detail_url, {'text_signature': 'newFunction()'})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_cannot_delete_signature(api_client, factories):
    signature = factories.SignatureFactory()
    detail_url = reverse('api:signature-detail', kwargs={'pk': signature.pk})

    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
