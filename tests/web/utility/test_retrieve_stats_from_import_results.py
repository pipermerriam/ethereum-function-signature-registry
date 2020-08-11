import pytest

from func_sig_registry.utils.abi import (
    retrieve_stats_from_import_results,
)

@pytest.mark.parametrize(
    'array_of_tuples,expected',
    (
        (
            [(None, False),(None, True),None,(None, True),(None, False)], 
            (5, 2, 2, 1)
        ),
        (#Empty Array
            [], 
            (0, 0, 0, 0)
        ),
        (#Only None
            [None, None, None, None], 
            (4, 0, 0, 4)
        ),
        (#No None
            [(None, True), (None, True), (None, True), (None, False), (None, False)], 
            (5, 3, 2, 0)
        ),
    ),
)
def test_retrieve_stats_from_import_results(array_of_tuples, expected):
    actual = retrieve_stats_from_import_results(array_of_tuples)
    assert actual == expected
