import codecs

from sha3 import sha3_256


def force_bytes(value):
    if isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return bytes(value, 'latin1')
    else:
        raise TypeError("Unsupported type: {0}".format(type(value)))


def force_text(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return str(value, 'latin1')
    else:
        raise TypeError("Unsupported type: {0}".format(type(value)))


def remove_0x_prefix(value):
    if force_bytes(value).startswith(b'0x'):
        return value[2:]
    return value


def encode_hex(value):
    return b'0x' + codecs.encode(force_bytes(value), 'hex')


def decode_hex(value):
    return codecs.decode(remove_0x_prefix(force_bytes(value)), 'hex')


def clean_text_signature(value):
    return value.strip().replace(' ', '').replace('\n', '').replace('\t', '')


# sanity check we are using the right sha3 function
assert sha3_256(b'').hexdigest() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', sha3_256(b'').hexdigest()  # NOQA


def make_4byte_signature(text_signature):
    return sha3_256(force_bytes(text_signature)).digest()[:4]
