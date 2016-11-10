pragma solidity ^0.4.0;


import {SignatureDBInterface} from "contracts/SignatureDBInterface.sol";
import {CanonicalSignatureLib} from "contracts/CanonicalSignatureLib.sol";
import {ArgumentLib} from "contracts/ArgumentLib.sol";
import {ArrayLib} from "contracts/ArrayLib.sol";



contract SignatureDB is SignatureDBInterface{
    using CanonicalSignatureLib for CanonicalSignatureLib.CanonicalSignature;
    using ArgumentLib for ArgumentLib.Argument;
    using ArrayLib for ArrayLib.Array;
    
    // signatureID => full canonical signature data.
    mapping (bytes32 => CanonicalSignatureLib.CanonicalSignature) signatures;

    // sha3(signature) => signatureID
    mapping (bytes32 => bytes32) hashToSignatureID;

    // signatureID => exists
    mapping (bytes32 => bool) knownSignatureIDs;

    // 4byte selector => signatureID[] array
    mapping (bytes4 => bytes32[]) selectorToSignatureHashes;

    /*
     * ------------------------------------:
     * addSignature(...) argument examples :
     * ------------------------------------:
     *  foo() -> _name: 'foo'
     *           dataTypes: []
     *           subs: []
     *           arrListLengths: []
     *           arrListsDynamic: []
     *           arrListsSize: []
     *
     *  foo(bytes32) -> _name: 'foo'
     *                  dataTypes: [ArgumentLib.DataType.BytesFixed]
     *                  subs: [32]
     *                  arrListLengths: [0]
     *                  arrListsDynamic: []
     *                  arrListsSize: []
     *
     *  foo(bytes32,uint256) -> _name: 'foo'
     *                          dataTypes: [
     *                              ArgumentLib.DataType.BytesFixed,
     *                              ArgumentLib.DataType.UInt,
     *                          ]
     *                          subs: [32, 256]
     *                          arrListLengths: [0, 0]
     *                          arrListsDynamic: []
     *                          arrListsSize: []
     *
     *  foo(bytes32,bool[][2],uint256) -> _name: 'foo'
     *                                    dataTypes: [
     *                                        ArgumentLib.DataType.BytesFixed,
     *                                        ArgumentLib.DataType.Bool,
     *                                        ArgumentLib.DataType.UInt,
     *                                    ]
     *                                    subs: [32, 0, 256]
     *                                    arrListLengths: [0, 2, 0]
     *                                    arrListsDynamic: [true, false]
     *                                    arrListsSize: [0, 2]
     */
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
                          uint[] arrListsSize) returns (bool) {
        bytes32 signatureID = sha3(_name,
                                   dataTypes,
                                   subs,
                                   arrListLengths,
                                   arrListsDynamic,
                                   arrListsSize);
        if (knownSignatureIDs[signatureID]) {
            return false;
        }

        var signature = signatures[signatureID];
        signature.init(_name,
                       dataTypes,
                       subs,
                       arrListLengths,
                       arrListsDynamic,
                       arrListsSize);
        if (signature.isValid()) {
            // compute the canonical signature string.
            signature.toString();

            // record that we know about this signature
            knownSignatureIDs[signatureID] = true;

            // compute the full signature hash and map it to the signature ID
            var signatureHash = sha3(signature.repr);
            hashToSignatureID[signatureHash] = signatureID;

            // Log the addition
            SignatureAdded(signatureHash);

            // compute the selector and map it to the signature hash
            var selector = bytes4(signatureHash);
            selectorToSignatureHashes[selector].push(signatureHash);

            // return success
            return true;
        } else {
            // zero the data back out if it was invalid.
            signature.reset();
            return false;
        }
    }

    /// @dev Returns whether the given signature is known by the DB
    /// @param signature String the canonical function signature.
    function isKnownSignature(string signature) constant returns (bool) {
        return knownSignatureIDs[hashToSignatureID[sha3(signature)]];
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
        return signatures[hashToSignatureID[signatureHash]].repr;
    }

    /// @dev Returns the canonical signature string.
    /// @param selector String the 4-byte fn selector.
    /// @param idx Number the 0-index of the signatureHash to return.
    function getSignature(bytes4 selector, uint idx) constant returns (string) {
        return getSignature(getSignatureHash(selector, idx));
    }
}
