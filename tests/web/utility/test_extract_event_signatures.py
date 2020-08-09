from func_sig_registry.utils.solidity import (
    extract_event_signatures,
)


CODE = """
contract Foo {
    // Empty Function
    event foo_1();

    // Abstract Function
    event foo_2();

    // single argument
    event foo_3(int a);

    // with return
    event foo_4(int a);

    // multiline
    event foo_5(int a,
                   int b,
                   int c);

    // awkward spacing
    event foo_6 ( int a );

    // touching braces
    event foo_7(int a);

    // commented out
    // event foo_8(address x);

    // contains indexed argugment
    event foo_9(int256 indexed a);
}
"""


def test_extract_event_signatures():
    signatures = extract_event_signatures(CODE)
    assert len(signatures) == 9
    assert set(signatures) == {
        'event foo_1()',
        'event foo_2()',
        'event foo_3(int a)',
        'event foo_4(int a)',
        'event foo_5(int a,\n                   int b,\n                   int c)',
        'event foo_6 ( int a )',
        'event foo_7(int a)',
        'event foo_8(address x)',
        'event foo_9(int256 indexed a)',
    }
