from rest_framework import status
from django.core.urlresolvers import reverse


CODE = """
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


def test_importing_solidity_source_code(api_client, factories):
    # function signature import expected stats:
    # processed: 8 | imported: 6 | duplicated: 2
    #
    # event signature import expected stats:
    # processed: 9 | imported: 9 | duplicated: 0
    # 
    # total:
    # processed: 17 | imported 15 | duplicated: 2
    factories.SignatureFactory(text_signature='foo_7(int256)')
    factories.SignatureFactory(text_signature='foo_6(int256)')

    import_url = reverse('api:import-solidity')

    response = api_client.post(import_url, {'source_code': CODE})

    assert response.status_code == status.HTTP_201_CREATED
    data = response.data
    assert data['num_processed'] == 17
    assert data['num_imported'] == 15
    assert data['num_duplicates'] == 2
