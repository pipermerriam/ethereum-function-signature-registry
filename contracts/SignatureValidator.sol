pragma solidity ^0.4.0;


import {SignatureDBInterface} from "./SignatureDBInterface.sol";
import {CanonicalSignatureLib} from "./CanonicalSignatureLib.sol";
import {ArgumentLib} from "./ArgumentLib.sol";
import {ArrayLib} from "./ArrayLib.sol";


contract SignatureValidator {
    using CanonicalSignatureLib for CanonicalSignatureLib.CanonicalSignature;
    using ArgumentLib for ArgumentLib.Argument;
    using ArrayLib for ArrayLib.Array;

    SignatureDBInterface public signatureDB;

    function SignatureValidator(address _signatureDB) {
        signatureDB = SignatureDBInterface(_signatureDB);
    }
    
    // A single storage variable so that we can use all the nice library functions.
    CanonicalSignatureLib.CanonicalSignature signature;

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
        signature.init(_name,
                       dataTypes,
                       subs,
                       arrListLengths,
                       arrListsDynamic,
                       arrListsSize);
        if (signature.isValid()) {
            // compute the canonical signature string.
            signature.toString();

            if (!signatureDB.isKnownSignature(signature.repr)) {
                signature.reset();
                return false;
            }

            if (signatureDB.addSignature(signature.repr)) {
                signature.reset();
                return true;
            }

        }

        // zero the data back out if it was invalid.
        signature.reset();
        return false;
    }
}
