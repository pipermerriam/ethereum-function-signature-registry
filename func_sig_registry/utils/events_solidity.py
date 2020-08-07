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

from func_sig_registry.utils.solidity import (
    get_arg_types,
    validate_standard_type,
    normalize_function_signature
)

EVENT_PARTS_RE = re.compile(r"""
^
\s*
(?:event\s+)?                     # optional leading "event" keyword
(?P<et_name>[a-zA-Z_][a-zA-Z0-9_]*)  # function name
\s*
\(                                   # opening paren before arg list
    (?P<arglist>.*)                  # argument list
\)                                   # closing paren after arg list
\s*
(?:anonymous)?                       # optional "anonymous" keyword
\s*
$
""", re.DOTALL | re.VERBOSE)


def extract_event_name(raw_signature):
    et_parts_match = EVENT_PARTS_RE.match(raw_signature)

    if et_parts_match is None:
        raise ValueError("Could not parse event signature")

    group_dict = et_parts_match.groupdict()
    et_name = group_dict['et_name']

    if et_name == 'event':
        raise ValueError("Bad event name")

    arglist = group_dict['arglist']

    return et_name, arglist


def validate_indexed_args(arglist: str):
    """
    Raise Exception if number of indexed arguments is greater than 3.
    Accepts only comma-delimited list of arguments
    """
    parts = arglist.split(',')
    indexed_amt = 0

    for p in parts:
        arg_parts = p.split()
        if( len(arg_parts) > 1 and arg_parts[1] == "indexed"):
            indexed_amt += 1
    
    if(indexed_amt > 3):
        raise ValueError("Too many indexed arguments")


def normalize_event_signature(raw_signature: str) -> str:
    """
    Return a normalized event signature from the input signature
    ``raw_signature``.  This function must return a normalized event
    signature or raise a ``ValueError``.
    """
    et_name, args = extract_event_name(raw_signature)

    #Check if number of indexed arguments is allowed
    validate_indexed_args(args)

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
        raise ValueError('event args contain non-standard types') from e
    else:
        return f'{et_name}{args_tuple_type.to_type_str()}'

#TODO
def extract_event_signatures(code):
    pass

#TODO
# "Name((uint, uint ))" - this doesn't work (with function also), decide what to do