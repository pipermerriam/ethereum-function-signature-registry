# Signature DB

The set of contracts housed in this repository make up an on-chain registry of
the data housed in the function signature database.  This is meant to serve as
a decentralized mirror to the existing database found at
[https://www.4byte.directory][https://www.4byte.directory].


## Terms

* **function signature**: The full function signature.  EG. `transfer(address _to, uint _value)`.
* **canonical function signature**: The canonical representation of the
  function signature. EG. `transfer(address,uint256)`
* **function selector**: The 4-byte value used by the EVM to select which
  function to call on a contract.  EG. `0xa9059cbb` which is the hex
  representation of the selector for the `transfer(address,uint256)` function.

# [`SignatureDB`](./SignatureDB.sol)

The `SignatureDB` contract is the user facing contract which exposes the
following functionality.

* Mapping from the 4-byte function selectors a list of known canonical function
  signatures.
* Querying for whether a 4-byte selector is known.
* Querying for whether a canonical function signature is known.
* Addition of new canonical function signatures which includes full
  validation that the signature being registered is in a valid canonical form.

## Structured Representation Of Canonical Signatures

The `SignatureDB` contract is designed to operate unpermissioned meaning that
anyone may submit new signatures to the database.  In order for this to be
possible it must be able to verify that submitted signatures are in their
canonical form.  To accomplish this, instead of submitting signatures as a
string, the contract requires them to be submitted in a format that allows the
contract to both verify that all components of the function signature are valid
after which it will construct the string representation of the canonical
signature on-chain.

The structured representation of a canonical function signature is defined as
follows.

### Function Name

The function name must match the regular expression `[a-zA-Z_][0-9a-zA-Z_]*`.


### Function Data Types

For each argument in the function signature we divide the data type into 3 components.

1. The base type without the size.
    * `bytes32 => bytes`
    * `uint128 => uint`
    * `int256 => int`
    * `bool => bool`
    * `address => address`
    * `bytes => bytes`
    * `string => string`
2. The size of the type.  For unsized types this must be `0`.
    * `bytes32 => 32`
    * `uint128 => 128`
    * `bool => 0`
    * `address => 0`
    * `bytes => 0`
    * `string => 0`
2. The array components of the type.  These are represented as an array of
   length-2 arrays where the first element denotes whether the array is
   dynamically sized or statically sized, and the second component denotes the
   size.  (Dynamically sized arrays must always have a size of 0).
    * `bytes32 => []`
    * `bytes32[] => [[true, 0]]`
    * `bytes32[][3] => [[true, 0], [false, 3]]`
    * `address[2][] => [[false, 2], [true, 0]]`

#### Base Types

The base type is represented in the smart contract with the following Enum.

```javascript
enum DataType {
    Null,
    Address,
    Bool,
    UInt,
    Int,
    BytesFixed,
    BytesDynamic,
    String
}
```

When submitting the base types for function arguments they must be converted to
the integer representation for the given type which are as follows.

* `address => DataType.Address => 1`
* `bool => DataType.Bool => 2`
* `uint => DataType.UInt => 3`
* `int => DataType.Int => 4`
* `bytes => DataType.BytesFixed => 5`: This is for fixed bytes values. eg. `bytes1, bytes2, ..., bytes32`.
* `bytes => DataType.BytesDynamic => 6`: This is for dynamic byte arrays: eg. `bytes`
* `string => DataType.String => 7`

The `Null` enum value is not used and will always fail validation.

#### Sub Types

The sub type component of an argument is merely the integer size of the
argument.

* `bytes32 => 32`
* `uint8 => 8`

This value must always be `0` for the unsized types `bool`, `bytes`, `string`, `address`


#### Array Component

For array types, each dimension of the array is represented by a `bool` and a `uint`.

The `bool` indicates whether it is a dynamic or fixed size array, with `true`
denoting that the array is dynamic in size (eg. `bytes32[]`) and `false`
denoting that the array is fixed size (eg. `bytes32[10]`).

The `uint` indicates the size of the array.  This value must be `0` for dynamic
arrays.

In order for the contract to parse this data it must be converted into 3 distinct arrays:

1. `uint[]` with the number of array elements for each argument
2. `bool[]` with the booleans denoting whether the array values are dynamic.
2. `uint[]` with the sizes of the array values.

For example:

* `foo(uint256[3])`:
    1. `[1]`: indicates that the 0th argument has 1 array component.
    2. `[false]`: indicates that the array component is of fixed size.
    3. `[3]`: indicates that the size of the array is `3`.
* `foo(uint256[3],address,bytes32[][2][])`:
    1. `[1, 0, 3]`: indicates that the 0th argument has 1 array component, that
       the 1st argument has no array components, and that the 2nd argument has 3
       array components.
    2. `[false, true, false, true]`: Since there are 4 total array components
       in this signature, this represents whether each component is dynamic or
       fixed.
    3. `[3, 0, 2, 0]`: The sizes of the 4 total array components.


### The `addSignature` function.

* **`function addSignature(string _name, uint[] dataTypes, uint[] subs, uint[] arrListLengths, bool[] arrListsDynamic, uint[] arrListsSize) returns (bool)`**

With these we can construct the arguments needed to call the `addSignature`
function which takes the following arguments.

* `string _name`: The name of the function.
* `uint[] dataTypes`: An array of all of the argument base types.
* `uint[] subs`: An array of all of the argument sub types.
* `uint[] arrListLengths`: An array with the number of array elements for each argument.
* `bool[] arrListsDynamic`: A flattened array of all of the boolean flags
  denoting whether the array is dynamic or fixed.
* `uint[] arrListsSize) returns (bool)`: A flattened array of all of the sizes
  of the array components of the types.


#### Examples

The following examples show how each of the given function signatures should be
decomposed for submission through the `addSignature` function.

* `foo()`:
    * `_name: 'foo'`
    * `dataTypes: []`
    * `subs: []`
    * `arrListLengths: []`
    * `arrListsDynamic: []`
    * `arrListsSize: []`
* `foo(bytes32)`:
    * `_name: 'foo'`
    * `dataTypes: [5]`
    * `subs: [32]`
    * `arrListLengths: [0]`
    * `arrListsDynamic: []`
    * `arrListsSize: []`
* `foo(bytes32,uint256)`
    * `_name: 'foo'`
    * `dataTypes: [5, 3]`
    * `subs: [32, 256]`
    * `arrListLengths: [0, 0]`
    * `arrListsDynamic: []`
    * `arrListsSize: []`
* `foo(bytes32,bool[][2],uint256)`
    * `_name: 'foo'`
    * `dataTypes: [5, 2, 3]`
    * `subs: [32, 0, 256]`
    * `arrListLengths: [0, 2, 0]`
    * `arrListsDynamic: [true, false]`
    * `arrListsSize: [0, 2]`
