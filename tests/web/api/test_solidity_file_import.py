from io import BytesIO
from rest_framework import status
from django.core.urlresolvers import reverse


CODE = b"""
contract Foo {
    // Empty Function
    function foo_1() {
    }

    // Abstract Function
    function foo_2();

    // single argument
    function foo_3(int a) {
    }

    // with return
    function foo_4(int a) returns (int) {
    }

    // multiline
    function foo_5(int a,
                   int b,
                   int c) {
    }

    // awkward spacing
    function foo_6 ( int a ) {
    }

    // touching braces
    function foo_7(int a){}

    // commented out
    // function foo_8(address x) {}
}
"""


def test_importing_solidity_source_file(api_client, factories):
    factories.SignatureFactory(text_signature='foo_7(int256)')
    factories.SignatureFactory(text_signature='foo_6(int256)')

    import_url = reverse('api:import-solidity')
    source_file = BytesIO(CODE)

    response = api_client.post(import_url, {'source_file': source_file}, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 8
    assert data['num_imported'] == 6
    assert data['num_duplicates'] == 2
