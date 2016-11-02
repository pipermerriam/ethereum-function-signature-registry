pragma solidity ^0.4.0;


contract SignatureDBInterface {
    event SignatureAdded(bytes32 indexed signatureHash);

    /// @dev Adds a signature to the database.
    /// @param canonicalSignature String the canonical function signature.
    function addSignature(string canonicalSignature) public returns (bool);

    /// @dev Returns whether the given signature is known by the DB
    /// @param signature String the canonical function signature.
    function isKnownSignature(string signature) constant returns (bool);

    /// @dev Returns whether the given selector is known by the DB
    /// @param selector String the 4-byte fn selector.
    function isKnownSelector(bytes4 selector) constant returns (bool);

    /// @dev Returns the number of known signatures for a given 4byte selector.
    /// @param selector String the 4-byte fn selector.
    function numSignatures(bytes4 selector) constant returns (uint);

    /// @dev Returns the signatureHash for the function signature at the given index.
    /// @param selector String the 4-byte fn selector.
    /// @param idx Number the 0-index of the signatureHash to return.
    function getSignatureHash(bytes4 selector,
                              uint idx) constant returns (bytes32);

    /// @dev Returns all signature IDs for the 4byte selector.
    /// @param selector String the 4-byte fn selector.
    function getAllSignatureHashes(bytes4 selector) constant returns (bytes32[]);

    /// @dev Returns the canonical signature string.
    /// @param signatureHash String the sha3(signature) for the function.
    function getSignature(bytes32 signatureHash) constant returns (string);

    /// @dev Returns the canonical signature string.
    /// @param selector String the 4-byte fn selector.
    /// @param idx Number the 0-index of the signatureHash to return.
    function getSignature(bytes4 selector, uint idx) constant returns (string);
}
