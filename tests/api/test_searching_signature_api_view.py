from rest_framework import status
from django.core.urlresolvers import reverse


def test_exact_hex_search(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature={0}'.format(s2.bytes_signature.get_hex_display())
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_exact_without_0x_hex_search(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature={0}'.format(s2.bytes_signature.get_hex_display()[2:])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_substring_hex_search_with_0x(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature={0}'.format(s2.bytes_signature.get_hex_display()[:6])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id


def test_substring_hex_search_without_0x(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature={0}'.format(s2.bytes_signature.get_hex_display()[2:6])
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 1
    assert len(data['results']) == 1

    result = data['results'][0]

    assert result['id'] == s2.id
