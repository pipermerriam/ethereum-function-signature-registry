from eth_abi.abi import process_type


class DataTypes(object):
    Null = 0
    Address = 1
    Bool = 2
    UInt = 3
    Int = 4
    BytesFixed = 5
    BytesDynamic = 6
    String = 7

    @classmethod
    def from_string(cls, type_string):
        base, sub, _ = process_type(type_string)
        if base == 'bytes':
            if sub:
                return cls.BytesFixed
            else:
                return cls.BytesDynamic
        elif base == 'string':
            return cls.String
        elif base == 'int':
            return cls.Int
        elif base == 'uint':
            return cls.UInt
        elif base == 'bool':
            return cls.Bool
        elif base == 'address':
            return cls.Address
        else:
            raise ValueError("Unknown type: {0}".format(type_string))


def function_definition_to_kwargs(function_abi):
    """
    Construct kwargs suitable for submitting a function signature to the
    signature DB
    """
    kwargs = {
        '_name': function_abi['name'],
        'dataTypes': [],
        'subs': [],
        'arrListLengths': [],
        'arrListsDynamic': [],
        'arrListsSize': [],
    }
    for argument_abi in function_abi['inputs']:
        kwargs['dataTypes'].append(DataTypes.from_string(argument_abi['type']))
        base, sub, arrlist = process_type(argument_abi['type'])
        if sub:
            kwargs['subs'].append(int(sub))
        else:
            kwargs['subs'].append(0)

        kwargs['arrListLengths'].append(len(arrlist))

        for arr_value in arrlist:
            kwargs['arrListsDynamic'].append(not bool(arr_value))
            if arr_value:
                kwargs['arrListsSize'].append(arr_value[0])
            else:
                kwargs['arrListsSize'].append(0)

    return kwargs
