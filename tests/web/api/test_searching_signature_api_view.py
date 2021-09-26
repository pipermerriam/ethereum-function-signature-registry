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


def test_multiple_exact_hex_search(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature__in={0},{1},{2}'.format(
        s2.bytes_signature.get_hex_display(),
        s4.bytes_signature.get_hex_display(),
        s5.bytes_signature.get_hex_display(),
    )
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 3
    actual_results = sorted([item['id'] for item in data['results']])
    assert len(actual_results) == 3
    expected_results = sorted([s2.id, s4.id, s5.id])
    assert actual_results == expected_results


def test_multiple_exact_without_0x_hex_search(api_client, factories):
    list_url = reverse('api:signature-list')
    s1, s2, s3, s4, s5 = factories.SignatureFactory.create_batch(5)

    search_url = list_url + '?hex_signature__in={0},{1},{2}'.format(
        s1.bytes_signature.get_hex_display()[2:],
        s3.bytes_signature.get_hex_display()[2:],
        s4.bytes_signature.get_hex_display()[2:],
    )
    response = api_client.get(search_url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data['count'] == 3
    actual_results = sorted([item['id'] for item in data['results']])
    assert len(actual_results) == 3
    expected_results = sorted([s1.id, s3.id, s4.id])
    assert actual_results == expected_results


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
