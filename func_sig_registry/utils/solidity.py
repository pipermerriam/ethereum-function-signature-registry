import itertools
import re
from typing import (
    List,
)

from eth_abi.exceptions import (
    ParseError,
    ABITypeError,
)
from eth_abi.grammar import (
    parse as parse_type,
    normalize as normalize_type,
    ABIType,
    TupleType,
    BasicType,
)


DYNAMIC_TYPES = ['bytes', 'string']

STATIC_TYPE_ALIASES = [
    'uint',
    'int',
    'ufixed',
    'fixed',
    'byte',
]

BITS_REGEX = r'(?:{})'.format('|'.join(str(i) for i in range(8, 257, 8)))
PLACES_REGEX = r'(?:{})'.format('|'.join(str(i) for i in range(1, 81)))

STATIC_TYPES = [
    'uint{0}'.format(BITS_REGEX),
    'int{0}'.format(BITS_REGEX),
    'address',
    'bool',
    'fixed{0}x{1}'.format(BITS_REGEX, PLACES_REGEX),
    'ufixed{0}x{1}'.format(BITS_REGEX, PLACES_REGEX),
] + ['bytes{0}'.format(i) for i in range(1, 33)]

TYPE_REGEX = '|'.join((
    _type + r'(?![a-z0-9])'
    for _type
    in itertools.chain(STATIC_TYPES, STATIC_TYPE_ALIASES, DYNAMIC_TYPES)
))

NAME_REGEX = (
    r'[a-zA-Z_]'
    r'[a-zA-Z0-9_]*'
)

SUB_TYPE_REGEX = (
    r'\['
    r'[0-9]*'
    r'\]'
)

FUNCTION_ARGUMENT_REGEX = (
    r'(?:{type})'
    r'(?:(?:{sub_type})*)?'
    r'\s+'
    '{name}'
).format(
    type=TYPE_REGEX,
    sub_type=SUB_TYPE_REGEX,
    name=NAME_REGEX,
)

EVENT_ARGUMENT_REGEX = (
    r'(?:{type})'
    r'(?:(?:{sub_type})*)?'
    r'(?:\s+indexed)?'
    r'\s+'
    '{name}'
).format(
    type=TYPE_REGEX,
    sub_type=SUB_TYPE_REGEX,
    name=NAME_REGEX,
)

RAW_FUNCTION_RE = re.compile(r"""
function                          # leading "function" keyword
\s+
{name}                            # function name
\s*
\(                                # opening paren before arg list
    \s*
    (?:
        {arg}                     # first arg in arg list
        (?:
            (?:\s*,\s*{arg}\s*)*  # other args in arg list
        )?
        (?:,)?                    # optional trailing comma in arg list
    )?                            # optional arg list
    \s*
\)                                # closing paren after arg list
""".format(name=NAME_REGEX, arg=FUNCTION_ARGUMENT_REGEX), re.VERBOSE)

RAW_EVENT_RE = re.compile(r"""
event                             # leading "event" keyword
\s+
{name}                            # event name
\s*
\(                                # opening paren before arg list
    \s*
    (?:
        {arg}                     # first arg in arg list
        (?:
            (?:\s*,\s*{arg}\s*)*  # other args in arg list
        )?
        (?:,)?                    # optional trailing comma in arg list
    )?                            # optional arg list
    \s*
\)                                # closing paren after arg list
(?:\s*anonymous)?                 # optional anonymous
""".format(name=NAME_REGEX, arg=EVENT_ARGUMENT_REGEX), re.VERBOSE)


def extract_function_signatures(code):
    """
    Given a string of solidity code, extract all of the function declarations.
    """
    matches = RAW_FUNCTION_RE.findall(code)
    return matches or []


def extract_event_signatures(code):
    """
    Given a string of solidity code, extract all of the event declarations,
    including anonymous
    """
    matches = RAW_EVENT_RE.findall(code)
    return matches or []


FUNCTION_PARTS_RE = re.compile(r"""
^
\s*
(?:function\s+)?                     # optional leading "function" keyword
(?P<fn_name>[a-zA-Z_][a-zA-Z0-9_]*)  # function name
\s*
\(                                   # opening paren before arg list
    (?P<arglist>.*)                  # argument list
\)                                   # closing paren after arg list
\s*
$
""", re.DOTALL | re.VERBOSE)


def extract_function_name(raw_signature):
    fn_parts_match = FUNCTION_PARTS_RE.match(raw_signature)

    if fn_parts_match is None:
        raise ValueError("Could not parse function signature")

    group_dict = fn_parts_match.groupdict()
    fn_name = group_dict['fn_name']

    if fn_name == 'function':
        raise ValueError("Bad function name")

    arglist = group_dict['arglist']

    return fn_name, arglist


STANDARD_BASE_TYPES = {
    'uint',
    'int',
    'address',
    'bool',
    'fixed',
    'ufixed',
    'bytes',
    'function',
    'string',
}


def validate_standard_type(abi_type: ABIType) -> None:
    """
    Assert that an abi type is standard.  A basic ABI type is standard if its
    type base is one of the standard ABI base types.  A tuple ABI type is
    standard if all basic types contained within it are standard.
    """
    if isinstance(abi_type, BasicType):
        if abi_type.base not in STANDARD_BASE_TYPES:
            raise ABITypeError(
                f'type "{abi_type.to_type_str()}" '
                f'has invalid base "{abi_type.base}"'
            )
    elif isinstance(abi_type, TupleType):
        for t in abi_type.components:
            validate_standard_type(t)
    else:
        raise Exception('unreachable branch arm')


def get_arg_types(arglist: str) -> List[str]:
    """
    Return a list of types from a comma-delimited list of type/name pairs.

    Example:
    >>> get_arg_types('  T   x, T.X y, int z, bool a , a')
    ['T', 'T.X', 'int', 'bool', 'a']
    """
    parts = arglist.split(',')
    types = [p.strip().split(maxsplit=1)[0] for p in parts]

    return types


def normalize_function_signature(raw_signature: str) -> str:
    """
    Return a normalized function signature from the input signature
    ``raw_signature`` that is suitable for generating a function selector via
    the Keccak hash function.  This function must return a normalized function
    signature or raise a ``ValueError``.
    """
    fn_name, args = extract_function_name(raw_signature)

    try:
        # Make arg list look like tuple and try to parse as normalized abi type
        args_tuple_type = parse_type(normalize_type(f'({args})'))
    except ParseError:
        # If not parseable, assume it's a solidity function signature, extract
        # types, and attempt to parse again
        arg_types = ','.join(get_arg_types(args))
        try:
            args_tuple_type = parse_type(normalize_type(f'({arg_types})'))
        except ParseError as e:
            raise ValueError('could not parse function args') from e

    # If args list parseable as abi type, do some validation and return string
    # representation
    try:
        # No custom ABI types
        validate_standard_type(args_tuple_type)
        # All basic types have expected properties
        args_tuple_type.validate()
    except ABITypeError as e:
        raise ValueError('function args contain non-standard types') from e
    else:
        return f'{fn_name}{args_tuple_type.to_type_str()}'