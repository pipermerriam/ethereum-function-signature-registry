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
        # Bytes (dynamic)
        (DataTypes.BytesDynamic, 0, [], True),
        (DataTypes.BytesDynamic, 1, [], False),  # sub must be 0
        (DataTypes.BytesDynamic, 0, [(True, 0)], True),
        (DataTypes.BytesDynamic, 0, [(True, 0), (True, 0)], True),
        (DataTypes.BytesDynamic, 0, [(True, 0), (False, 25)], True),
        (DataTypes.BytesDynamic, 0, [(True, 0), (True, 1)], False),  # invalid arrlist
        # String
        (DataTypes.String, 0, [], True),
        (DataTypes.String, 1, [], False),  # sub must be 0
        (DataTypes.String, 0, [(True, 0)], True),
        (DataTypes.String, 0, [(True, 0), (True, 0)], True),
        (DataTypes.String, 0, [(True, 0), (False, 25)], True),
        (DataTypes.String, 0, [(True, 0), (True, 1)], False),  # invalid arrlist
        # Bool
        (DataTypes.Bool, 0, [], True),
        (DataTypes.Bool, 1, [], False),  # sub must be 0
        (DataTypes.Bool, 0, [(True, 0)], True),
        (DataTypes.Bool, 0, [(True, 0), (True, 0)], True),
        (DataTypes.Bool, 0, [(True, 0), (False, 25)], True),
        (DataTypes.Bool, 0, [(True, 0), (True, 1)], False),  # invalid arrlist
        # Uint
        (DataTypes.UInt, 0, [], False),  # sub must be [8, 256]
        (DataTypes.UInt, 1, [], False),  # sub must be [8, 256]
        (DataTypes.UInt, 7, [], False),  # sub must be [8, 256]
        (DataTypes.UInt, 8, [], True),
        (DataTypes.UInt, 9, [], False),  # sub must be multiple of 8
        (DataTypes.UInt, 15, [], False),  # sub must be multiple of 8
        (DataTypes.UInt, 32, [], True),
        (DataTypes.UInt, 128, [], True),
        (DataTypes.UInt, 256, [], True),
        (DataTypes.UInt, 256, [(True, 0)], True),
        (DataTypes.UInt, 256, [(True, 0), (True, 0)], True),
        (DataTypes.UInt, 256, [(True, 0), (False, 25)], True),
        (DataTypes.UInt, 256, [(True, 0), (True, 1)], False),  # invalid arrlist
        # Int
        (DataTypes.Int, 0, [], False),  # sub must be [8, 256]
        (DataTypes.Int, 1, [], False),  # sub must be [8, 256]
        (DataTypes.Int, 7, [], False),  # sub must be [8, 256]
        (DataTypes.Int, 8, [], True),
        (DataTypes.Int, 9, [], False),  # sub must be multiple of 8
        (DataTypes.Int, 15, [], False),  # sub must be multiple of 8
        (DataTypes.Int, 32, [], True),
        (DataTypes.Int, 128, [], True),
        (DataTypes.Int, 256, [], True),
        (DataTypes.Int, 256, [(True, 0)], True),
        (DataTypes.Int, 256, [(True, 0), (True, 0)], True),
        (DataTypes.Int, 256, [(True, 0), (False, 25)], True),
        (DataTypes.Int, 256, [(True, 0), (True, 1)], False),  # invalid arrlist
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
        # Bytes (dynamic)
        (DataTypes.BytesDynamic, 0, [], 'bytes'),
        (DataTypes.BytesDynamic, 0, [(True, 0)], 'bytes[]'),
        (DataTypes.BytesDynamic, 0, [(True, 0), (True, 0)], 'bytes[][]'),
        (DataTypes.BytesDynamic, 0, [(True, 0), (False, 25)], 'bytes[][25]'),
        # Bytes (dynamic)
        (DataTypes.String, 0, [], 'string'),
        (DataTypes.String, 0, [(True, 0)], 'string[]'),
        (DataTypes.String, 0, [(True, 0), (True, 0)], 'string[][]'),
        (DataTypes.String, 0, [(True, 0), (False, 25)], 'string[][25]'),
        # Bool
        (DataTypes.Bool, 0, [], 'bool'),
        (DataTypes.Bool, 0, [(True, 0)], 'bool[]'),
        (DataTypes.Bool, 0, [(True, 0), (True, 0)], 'bool[][]'),
        (DataTypes.Bool, 0, [(True, 0), (False, 25)], 'bool[][25]'),
        # Uint
        (DataTypes.UInt, 8, [], 'uint8'),
        (DataTypes.UInt, 32, [], 'uint32'),
        (DataTypes.UInt, 128, [], 'uint128'),
        (DataTypes.UInt, 256, [], 'uint256'),
        (DataTypes.UInt, 256, [(True, 0)], 'uint256[]'),
        (DataTypes.UInt, 256, [(True, 0), (True, 0)], 'uint256[][]'),
        (DataTypes.UInt, 256, [(True, 0), (False, 25)], 'uint256[][25]'),
        # Int
        (DataTypes.Int, 8, [], 'int8'),
        (DataTypes.Int, 32, [], 'int32'),
        (DataTypes.Int, 128, [], 'int128'),
        (DataTypes.Int, 256, [], 'int256'),
        (DataTypes.Int, 256, [(True, 0)], 'int256[]'),
        (DataTypes.Int, 256, [(True, 0), (True, 0)], 'int256[][]'),
        (DataTypes.Int, 256, [(True, 0), (False, 25)], 'int256[][25]'),
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
