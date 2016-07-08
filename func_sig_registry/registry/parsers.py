import itertools
import re


DYNAMIC_TYPES = ['bytes', 'string']

STATIC_TYPE_ALIASES = ['uint', 'int', 'byte']
STATIC_TYPES = list(itertools.chain(
    ['address', 'bool'],
    ['uint{0}'.format(i) for i in range(8, 257, 8)],
    ['int{0}'.format(i) for i in range(8, 257, 8)],
    ['bytes{0}'.format(i) for i in range(1, 33)],
))

TYPE_REGEX = '|'.join(itertools.chain(
    DYNAMIC_TYPES,
    STATIC_TYPES,
    STATIC_TYPE_ALIASES,
))

NAME_REGEX = '[a-zA-Z_][a-zA-Z0-9_]*'

ARGUMENT_REGEX = '(?:{type})(?:(?:\[[0-9]*\])*)?\s+[a-zA-Z_][a-zA-Z0-9_]*'.format(
    type=TYPE_REGEX,
)


FUNCTION_REGEX = (
    'function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*(?:{arg}(?:(?:\s*,\s*{arg}\s*)*)?)?\s*\)'.format(
        arg=ARGUMENT_REGEX,
    )
)


def extract_function_signatures(code):
    matches = re.findall(FUNCTION_REGEX, code)
    return matches or []


EXTRACT_ARGUMENTS_REGEX = (
    '(?P<type>{type})(?P<sub_type>(?:\[[0-9]*\])*)?\s+[a-zA-Z_][a-zA-Z0-9_]*'.format(
        type=TYPE_REGEX,
    )
)


def to_canonical_type(value):
    if value == 'int':
        return 'int256'
    elif value == 'uint':
        return 'uint256'
    elif value == 'byte':
        return 'bytes1'
    else:
        return value


def normalize_function_signature(raw_signature):
    fn_name_match = re.match('function\s+(?P<fn_name>[a-zA-Z_][a-zA-Z0-9_]*)', raw_signature)
    group_dict = fn_name_match.groupdict()
    fn_name = group_dict['fn_name']
    raw_arguments = re.findall(EXTRACT_ARGUMENTS_REGEX, raw_signature)

    arguments = [
        "".join((to_canonical_type(t), sub))
        for t, sub in raw_arguments
    ]
    return "{fn_name}({fn_args})".format(fn_name=fn_name, fn_args=','.join(arguments))
