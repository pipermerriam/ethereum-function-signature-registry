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

    // fixed types
    function foo_9(fixed a, ufixed b){}

    struct T {
        int x;
        int y;
    }

    // functions with struct args ignored
    function foo_10(T a, ufixed b){}

    // functions with non-standard type args ignored
    function foo_11(bar a, ufixed b){}

    // empty event
    event bar_1();

    // event with one argument (normalized)
    event bar_2(uint256 a);

    // event with one argument (not normalized)
    event bar_3(uint a);

    // event with indexed argument
    event bar_4(address indexed a);

    // event with dynamic type argument
    event bar_5(bytes[32] a);

    // event with dynamic and indexex argument
    event bar_6(bytes[32] indexed a);

    // werid spacing
    event bar_7  ( address from,address to ) ;

    // weird spacing and mutlitline (2)
    event bar_8 (
        uint a,
        uint b,
        uint c
    );

    // commented event
    // event bar_9(uint8 b);

    // invalid event, wrong argument type (ignored)
    event bar_10(function a);

    // invalid, wrong argument delimeter (ignored)
    event bar_10(uint a; uint b);
}
"""


def test_importing_solidity_source_file(api_client, factories):
    # function signature import expected stats:
    # processed: 9 | imported: 7 | duplicated: 2
    #
    # event signature import expected stats:
    # processed: 9 | imported: 9 | duplicated: 0
    # 
    # total:
    # processed: 18 | imported 16 | duplicated: 2
    factories.SignatureFactory(text_signature='foo_7(int256)')
    factories.SignatureFactory(text_signature='foo_6(int256)')

    import_url = reverse('api:import-solidity')
    source_file = BytesIO(CODE)

    response = api_client.post(import_url, {'source_file': source_file}, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 18
    assert data['num_imported'] == 16
    assert data['num_duplicates'] == 2
