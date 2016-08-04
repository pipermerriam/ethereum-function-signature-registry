import codecs


def force_bytes(value):
    if isinstance(value, bytes):
        return value
    elif isinstance(value, memoryview):
        return bytes(value)
    elif isinstance(value, str):
        return bytes(value, 'utf8')
    else:
        raise TypeError("Unsupported type: {0}".format(type(value)))


def force_text(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return str(value, 'latin1')
    elif isinstance(value, memoryview):
        return str(bytes(value), 'latin1')
    else:
        raise TypeError("Unsupported type: {0}".format(type(value)))


def remove_0x_prefix(value):
    if force_bytes(value).startswith(b'0x'):
        return value[2:]
    return value


def add_0x_prefix(value):
    if force_bytes(value).startswith(b'0x'):
        return force_bytes(value)
    return b'0x' + force_bytes(value)


def encode_hex(value):
    return b'0x' + codecs.encode(force_bytes(value), 'hex')


def decode_hex(value):
    return codecs.decode(remove_0x_prefix(force_bytes(value)), 'hex')
