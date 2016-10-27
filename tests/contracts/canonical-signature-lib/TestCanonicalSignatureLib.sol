pragma solidity ^0.4.0;

import {CanonicalSignatureLib} from "contracts/CanonicalSignatureLib.sol";
import {ArgumentLib} from "contracts/ArgumentLib.sol";
import {ArrayLib} from "contracts/ArrayLib.sol";


contract TestCanonicalSignatureLib {
    using CanonicalSignatureLib for CanonicalSignatureLib.CanonicalSignature;
    using ArgumentLib for ArgumentLib.Argument;
    using ArrayLib for ArrayLib.Array;

    CanonicalSignatureLib.CanonicalSignature public value;

    function set(string _name,
                 uint[] dataTypes,
                 uint[] subs,
                 uint[] arrListLengths,
                 bool[] arrListsDynamic,
                 uint[] arrListsSize) returns (bool) {
        value.init(_name, dataTypes, subs, arrListLengths, arrListsDynamic, arrListsSize);
        if (value.isValid()) {
            value.toString();
            return true;
        }
        return false;
    }

    function getArgument(uint i) constant returns (uint dataType,
                                                   uint sub) {
        return value.arguments[i].serialize();
    }

    function getArrlist(uint i, uint j) constant returns (bool isDynamic,
                                                          uint size) {
        return value.arguments[i].arrList[j].serialize();
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
