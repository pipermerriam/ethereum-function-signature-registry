from sha3 import sha3_256


# sanity check we are using the right sha3 function
assert sha3_256(b'').hexdigest() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', sha3_256(b'').hexdigest()  # NOQA


def make_4byte_signature(text_signature):
    from .encoding import force_bytes
    return sha3_256(force_bytes(text_signature)).digest()[:4]
