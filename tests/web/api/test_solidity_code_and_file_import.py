from io import BytesIO
from rest_framework import status
from django.core.urlresolvers import reverse


CODE = """
contract Foo {
    function foo_1(uint a) {
    }

    event foo_2(uint a);
}
"""

FILE = b"""
contract Bar {
    function bar_1(uint a) {

    }

    event bar_2(uint a);
}
"""


def test_importing_solidity_source_code(api_client, factories):
    import_url = reverse('api:import-solidity')
    source_file = BytesIO(FILE)

    response = api_client.post(import_url, {
        'source_code': CODE,
        'source_file': source_file,
    }, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 4
    assert data['num_imported'] == 4
    assert data['num_duplicates'] == 0
    assert data['num_ignored'] == 0
