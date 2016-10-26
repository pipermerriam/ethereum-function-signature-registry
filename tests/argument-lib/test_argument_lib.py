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
        # Addresses
        (DataTypes.Address, 0, [], True),
        (DataTypes.Address, 1, [], False),  # address has no sub
        (DataTypes.Address, 0, [(True, 0)], True),
        (DataTypes.Address, 0, [(True, 1)], False),  # invalid arrlist
        (DataTypes.Address, 0, [(True, 0), (False, 10)], True),
        # Bytes (fixed)
        (DataTypes.BytesFixed, 0, [], False),  # sub must be between [1, 32]
        (DataTypes.BytesFixed, 33, [], False),  # sub must be between [1, 32]
        (DataTypes.BytesFixed, 1, [], True),
        (DataTypes.BytesFixed, 2, [], True),
        (DataTypes.BytesFixed, 15, [], True),
        (DataTypes.BytesFixed, 32, [], True),
        (DataTypes.BytesFixed, 32, [(True, 0)], True),
        (DataTypes.BytesFixed, 32, [(True, 0), (True, 0)], True),
        (DataTypes.BytesFixed, 32, [(True, 0), (False, 25)], True),
        (DataTypes.BytesFixed, 32, [(True, 0), (True, 1)], False),  # invalid arrlist
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


@pytest.mark.parametrize(
    'data_type,sub,arr_list,expected',
    (
        # Addresses
        (DataTypes.Address, 0, [], 'address'),
        (DataTypes.Address, 0, [(True, 0)], 'address[]'),
        (DataTypes.Address, 0, [(True, 0), (False, 10)], 'address[][10]'),
        # Bytes (fixed)
        (DataTypes.BytesFixed, 1, [], 'bytes1'),
        (DataTypes.BytesFixed, 2, [], 'bytes2'),
        (DataTypes.BytesFixed, 15, [], 'bytes15'),
        (DataTypes.BytesFixed, 32, [], 'bytes32'),
        (DataTypes.BytesFixed, 32, [(True, 0)], 'bytes32[]'),
        (DataTypes.BytesFixed, 32, [(True, 0), (True, 0)], 'bytes32[][]'),
        (DataTypes.BytesFixed, 32, [(True, 0), (False, 25)], 'bytes32[][25]'),
    ),
)
def test_argument_lib_repr(chain,
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

    assert test_argument_lib.call().isValid() is True
    assert test_argument_lib.call().repr() == expected
