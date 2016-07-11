from rest_framework import status
from django.core.urlresolvers import reverse


ABI = '[{"constant":false,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"int256"},{"name":"","type":"address"}],"name":"c","outputs":[],"type":"function"},{"constant":false,"inputs":[],"name":"f","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"","type":"int256"},{"name":"","type":"int256"}],"name":"b","outputs":[],"type":"function"},{"inputs":[],"type":"constructor"},{"anonymous":false,"inputs":[],"name":"E","type":"event"}]'


def test_importing_contract_abi(api_client, factories):
    factories.SignatureFactory(text_signature='b(int256,int256)')

    import_url = reverse('api:import-abi')

    response = api_client.post(import_url, {'contract_abi': ABI})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 3
    assert data['num_imported'] == 2
    assert data['num_duplicates'] == 1
