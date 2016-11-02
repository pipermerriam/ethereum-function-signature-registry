pragma solidity ^0.4.0;

import {authorized} from "./authorized.sol";
import {SignatureDBInterface} from "./SignatureDBInterface.sol";


contract SignatureDB is SignatureDBInterface, authorized {
    // sha3(canonicalSignature) => bool (isKnown)
    mapping (bytes32 => bool) knownCanonicalSignatures;

    // sha3(canonicalSignature) => bool (isKnown)
    mapping (bytes32 => string) canonicalSignatures;

    // 4byte selector => signatureID[] array
    mapping (bytes4 => bytes32[]) selectorToSignatureHashes;


    /// @dev Adds a signature to the database.
    /// @param canonicalSignature String the canonical function signature.
    function addSignature(string canonicalSignature) public auth returns (bool) {
        bytes32 signatureHash = sha3(canonicalSignature);
        if (knownCanonicalSignatures[signatureHash]) {
            return false;
        }
        bytes4 selector = bytes4(signatureHash);

        selectorToSignatureHashes[selector].push(signatureHash);
        canonicalSignatures[signatureHash] = canonicalSignature;
    }

    /// @dev Returns whether the given signature is known by the DB
    /// @param signature String the canonical function signature.
    function isKnownSignature(string signature) constant returns (bool) {
        return knownCanonicalSignatures[sha3(signature)];
    }

    /// @dev Returns whether the given selector is known by the DB
    /// @param selector String the 4-byte fn selector.
    function isKnownSelector(bytes4 selector) constant returns (bool) {
        return selectorToSignatureHashes[selector].length != 0;
    }

    /// @dev Returns the number of known signatures for a given 4byte selector.
    /// @param selector String the 4-byte fn selector.
    function numSignatures(bytes4 selector) constant returns (uint) {
        return selectorToSignatureHashes[selector].length;
    }

    /// @dev Returns the signatureHash for the function signature at the given index.
    /// @param selector String the 4-byte fn selector.
    /// @param idx Number the 0-index of the signatureHash to return.
    function getSignatureHash(bytes4 selector,
                              uint idx) constant returns (bytes32) {
        return selectorToSignatureHashes[selector][idx];
    }

    /// @dev Returns all signature IDs for the 4byte selector.
    /// @param selector String the 4-byte fn selector.
    function getAllSignatureHashes(bytes4 selector) constant returns (bytes32[]) {
        return selectorToSignatureHashes[selector];
    }

    /// @dev Returns the canonical signature string.
    /// @param signatureHash String the sha3(signature) for the function.
    function getSignature(bytes32 signatureHash) constant returns (string) {
        return canonicalSignatures[signatureHash];
    }

    /// @dev Returns the canonical signature string.
    /// @param selector String the 4-byte fn selector.
    /// @param idx Number the 0-index of the signatureHash to return.
    function getSignature(bytes4 selector, uint idx) constant returns (string) {
        return getSignature(getSignatureHash(selector, idx));
    }
}
