import pytest


class DataTypes(object):
    Null = 0
    Address = 1
    Bool = 2
    UInt = 3
    Int = 4
    BytesFixed = 5
    BytesDynamic = 6
    String = 7


@pytest.mark.parametrize(
    'data_type,sub,arr_list,expected',
    (
        (DataTypes.Address, 0, [], True),
        (DataTypes.Address, 1, [], False),  # address has no sub
        (DataTypes.Address, 0, [(True, 0)], True),
        (DataTypes.Address, 0, [(True, 1)], False),  # invalid arrlist
        (DataTypes.Address, 0, [(True, 0), (False, 10)], True),
    ),
)
def test_argument_lib_validation(chain,
                                 test_argument_lib,
                                 data_type,
                                 sub,
                                 arr_list,
                                 expected):
    if arr_list:
        arr_list_is_dynamic, arr_list_size = map(list, zip(*arr_list))
    else:
        arr_list_is_dynamic = []
        arr_list_size = []

    chain.wait.for_receipt(test_argument_lib.transact().reset())

    chain.wait.for_receipt(test_argument_lib.transact().set(
        dataType=data_type,
        sub=sub,
        arrListDynamic=arr_list_is_dynamic,
        arrListSize=arr_list_size,
    ))

    assert test_argument_lib.call().isValid() is expected
