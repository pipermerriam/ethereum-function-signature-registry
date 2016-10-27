pragma solidity ^0.4.0;

import {CanonicalSignatureLib} from "contracts/CanonicalSignatureLib.sol";


contract TestCanonicalSignatureLib {
    using CanonicalSignatureLib for CanonicalSignatureLib.CanonicalSignature;

    CanonicalSignatureLib.CanonicalSignature value;

    function set(string _name,
                 uint[] dataTypes,
                 uint[] subs,
                 bool[] arrListsDynamic,
                 uint[] arrListsSize) returns (bool) {
        value.init(_name, dataTypes, subs, arrListsDynamic, arrListsSize);
        if (value.isValid()) {
            value.toString();
            return true;
        }
        return false;
    }

    function isValid() constant returns (bool) {
        return value.isValid();
    }

    function repr() constant returns (string) {
        return value.repr;
    }

    function selector() constant returns (bytes4) {
        return value.selector;
    }
}
