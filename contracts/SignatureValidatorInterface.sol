pragma solidity ^0.4.0;


contract SignatureDBInterface {
    /// @dev Adds a new signature to the database
    /// @param _name String the fn name.
    /// @param dataTypes Array base types for the fn arguments.
    /// @param subs Array sub types for the fn arguments.
    /// @param arrListLengths Array the number of array elements for each fn argument
    /// @param arrListsDynamic Array whether the array is dynamic or static sized.
    /// @param arrListsSize Array the size of the array if static. Must be 0 if dynamic.
    function addSignature(string _name,
                          uint[] dataTypes,
                          uint[] subs,
                          uint[] arrListLengths,
                          bool[] arrListsDynamic,
                          uint[] arrListsSize) returns (bool);
}
