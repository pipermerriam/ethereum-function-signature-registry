import pytest

from func_sig_registry.registry.filters import EventSignatureFilter

# Sample data to populate the database (key -> text_signature)
TEST_EVENT_DATA = {
    'asd': 'asd(int256,int256)',
    'bsd': 'bsd(int256,int256)',
    'dsa': 'dsa(uint, uint indexed, string)',
    'foo': 'foo(address, string, uint)',
}


# expected is array of keys of TEST_EVENT_DATA
@pytest.mark.parametrize(
    'filter_data,expected',
    (
        # full text_signature
        ({'text_signature': 'asd(int256,int256)'},
         ['asd']),

        # partial text_signature
        ({'text_signature': 'asd'},
         ['asd']),

        # partial text_signature with multiple results
        ({'text_signature': 'sd'},
         ['asd', 'bsd']),

        # text_signature with empty result
        ({'text_signature': 'qwerty'},
         []),

        # full hex_signature
        ({'hex_signature': '1484d385b26b57c843ba735623eb866d226e6fc37fae7b665e3696e9544cf3e9'},
         ['asd']),

        # partial hex_signature
        ({'hex_signature': '1484d385b26b57'},
         ['asd']),

        # hex_signature with empty result
        ({'hex_signature': '1484d385b26b57c843ba735623eb866d226e6fc37fae7b665e3696e9544cf3e1'},
         []),
    ),
)
def test_event_signature_filter_by_text_hex_signature(factories, filter_data, expected):
    signature_dict = {}
    for key, value in TEST_EVENT_DATA.items():
        signature_dict[key] = factories.EventSignatureFactory(
            text_signature=value)

    event_filter = EventSignatureFilter(data=filter_data)

    assert len(event_filter.qs) == len(expected)

    for value in expected:
        assert signature_dict[value] in event_filter.qs


def test_event_signature_filter_by_bytes_signature(factories):
    for key, value in TEST_EVENT_DATA.items():
        event_signature = factories.EventSignatureFactory(
            text_signature=value)

        event_filter = EventSignatureFilter(data={
            'bytes_signature': event_signature.bytes_signature})

        assert len(event_filter.qs) == 1
        assert event_signature in event_filter.qs
