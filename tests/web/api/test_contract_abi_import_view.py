from rest_framework import status
from django.core.urlresolvers import reverse


ABI = '[{"constant":false,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"int256"},{"name":"","type":"address"}],"name":"c","outputs":[],"type":"function"},{"constant":false,"inputs":[],"name":"f","outputs":[],"type":"function"},{"constant":false,"inputs":[{"name":"","type":"int256"},{"name":"","type":"int256"}],"name":"b","outputs":[],"type":"function"},{"inputs":[],"type":"constructor"},{"anonymous":false,"inputs":[],"name":"E","type":"event"}]'

MY_ABI = """
[
    {"constant":false,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"int256"},{"name":"","type":"address"}],"name":"c","outputs":[],"type":"function"},
    {"constant":false,"inputs":[],"name":"f","outputs":[],"type":"function"},
    {"constant":false,"inputs":[{"name":"","type":"int256"},{"name":"","type":"int256"}],"name":"b","outputs":[],"type":"function"},
    {"inputs":[],"type":"constructor"},
    {"anonymous":false,"inputs":[{"name":"", "type":"string", "indexed":true}],"name":"E","type":"event"},
    {"anonymous":false,"inputs":[{"name":"", "type":"strong", "indexed":true}],"name":"Error","type":"event"},
    {"constant":false,"inputs":[{"name":"", "type":"myint"}],"name":"ErrorF","outputs":[],"type":"function"}
]
"""

def test_importing_contract_abi(api_client, factories):
    factories.SignatureFactory(text_signature='b(int256,int256)')

    import_url = reverse('api:import-abi')

    response = api_client.post(import_url, {'contract_abi': MY_ABI})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 6
    assert data['num_imported'] == 3
    assert data['num_duplicates'] == 1
    assert data['num_ignored'] == 2

