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

CANONICAL_TYPE_REGEX = '(' + '|'.join(itertools.chain(
    DYNAMIC_TYPES,
    STATIC_TYPES,
)) + ')'

NAME_REGEX = '[a-zA-Z_][a-zA-Z0-9_]*'

ARGUMENT_REGEX = '(?:{type})(?:(?:\[[0-9]*\])*)?\s+[a-zA-Z_][a-zA-Z0-9_]*'.format(
    type=TYPE_REGEX,
)


RAW_FUNCTION_REGEX = (
    'function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(\s*(?:{arg}(?:(?:\s*,\s*{arg}\s*)*)?)?\s*\)'.format(
        arg=ARGUMENT_REGEX,
    )
)


FUNCTION_ARGUMENTS_REGEX = (
    '(?P<type>{type})(?P<sub_type>(?:\[[0-9]*\])*)?(?:\s+[a-zA-Z_][a-zA-Z0-9_]*)?'.format(
        type=TYPE_REGEX,
    )
)


NORM_FUNCTION_REGEX = (
    '^'
    '[a-zA-Z_][a-zA-Z0-9_]*'
    '\('
    '('
    '{type}((\[[0-9]*\])*)'
    '('
    '(,{type}((\[[0-9]*\])*)?)*'
    ')?'
    ')?'
    '\)'
    '$'
).format(type=CANONICAL_TYPE_REGEX)


def is_raw_function_signature(signature):
    if re.fullmatch('^' + RAW_FUNCTION_REGEX + '$', signature):
        return True
    else:
        return False


def is_canonical_function_signature(signature):
    if re.fullmatch(NORM_FUNCTION_REGEX, signature):
        return True
    else:
        return False


def extract_function_signatures(code):
    """
    Given a string of solidity code, extract all of the function declarations.
    """
    matches = re.findall(RAW_FUNCTION_REGEX, code)
    return matches or []


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
    fn_name_match = re.match(
        '^(?:function\s+)?\s*(?P<fn_name>[a-zA-Z_][a-zA-Z0-9_]*).*\(.*\).*$',
        raw_signature,
        flags=re.DOTALL,
    )
    if fn_name_match is None:
        raise ValueError("Did not match function name")
    group_dict = fn_name_match.groupdict()
    fn_name = group_dict['fn_name']

    if fn_name == 'function':
        raise ValueError("Bad function name")
    raw_arguments = re.findall(FUNCTION_ARGUMENTS_REGEX, raw_signature)

    arguments = [
        "".join((to_canonical_type(t), sub))
        for t, sub in raw_arguments
    ]
    return "{fn_name}({fn_args})".format(fn_name=fn_name, fn_args=','.join(arguments))
