from sha3 import sha3_256

from jsonschema import (
    validate,
    ValidationError,
)


# sanity check we are using the right sha3 function
assert sha3_256(b'').hexdigest() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470', sha3_256(b'').hexdigest()  # NOQA


def make_4byte_signature(text_signature):
    from .encoding import force_bytes
    return sha3_256(force_bytes(text_signature)).digest()[:4]


ARGUMENT_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'type': {
            'type': 'string',
        },
    },
    'required': ['name', 'type'],
}


NAME = {'type': 'string'}
BOOLEAN = {'type': 'boolean'}
INPUTS = OUTPUTS = {'type': 'array', 'items': {'$ref': '#/definitions/argument'}}
EVENT_TYPE = {'type': 'string', 'enum': ['event']}
CONSTRUCTOR_TYPE = {'type': 'string', 'enum': ['constructor']}

FUNCTION_SCHEMA = {
    'type': 'object',
    'properties': {
        'constant': BOOLEAN,
        'type': {'type': 'string', 'enum': ['function']},
        'inputs': INPUTS,
        'outputs': OUTPUTS,
        'name': NAME,
    },
    'required': ['constant', 'type', 'inputs', 'outputs', 'name'],
    'definitions': {
        'argument': ARGUMENT_SCHEMA,
    },
}

EVENT_SCHEMA = {
    'type': 'object',
    'properties': {
        'anonymous': BOOLEAN,
        'type': {'type': 'string', 'enum': ['event']},
        'inputs': INPUTS,
        'name': NAME,
    },
    'required': ['type', 'inputs', 'name'],
    'definitions': {
        'argument': ARGUMENT_SCHEMA,
    },
}

CONSTRUCTOR_SCHEMA = {
    'type': 'object',
    'properties': {
        'type': {'type': 'string', 'enum': ['constructor']},
        'inputs': INPUTS,
    },
    'required': ['type', 'inputs'],
    'definitions': {
        'argument': ARGUMENT_SCHEMA,
    },
}

CONTRACT_ABI_SCHEMA = {
    'type': 'array',
    'items': {
        'anyOf': [
            {'$ref': '#/definitions/function'},
            {'$ref': '#/definitions/event'},
            {'$ref': '#/definitions/constructor'},
        ],
    },
    'definitions': {
        'function': FUNCTION_SCHEMA,
        'event': EVENT_SCHEMA,
        'constructor': CONSTRUCTOR_SCHEMA,
        'argument': ARGUMENT_SCHEMA,
    }
}


def is_valid_contract_abi(contract_abi):
    try:
        validate(contract_abi, CONTRACT_ABI_SCHEMA)
    except ValidationError:
        return False
    else:
        return True


def function_definition_to_text_signature(function_definition):
    return "{fn_name}({fn_input_types})".format(
        fn_name=function_definition['name'],
        fn_input_types=','.join([
            input['type'] for input in function_definition.get('inputs', [])
        ]),
    )
