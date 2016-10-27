pragma solidity ^0.4.0;

import {CharLib} from "contracts/CharLib.sol";
import {StringLib} from "contracts/StringLib.sol";
import {ArrayLib} from "contracts/ArrayLib.sol";
import {ArgumentLib} from "contracts/ArgumentLib.sol";


library CanonicalSignatureLib {
    using CharLib for bytes1;
    using StringLib for string;
    using ArrayLib for ArrayLib.Array;
    using ArgumentLib for ArgumentLib.Argument;

    struct CanonicalSignature {
        string name;
        string repr;
        bytes4 selector;
        ArgumentLib.Argument[] arguments;
    }

    function reset(CanonicalSignature storage self) returns (bool) {
        self.name = '';
        self.repr = '';
        self.selector = 0x0;
        self.arguments.length = 0;
    }

    function init(CanonicalSignature storage self,
                  string _name,
                  uint[] dataTypes,
                  uint[] subs,
                  bool[] arrListsDynamic,
                  uint[] arrListsSize) returns (bool) {
        reset(self);

        if (dataTypes.length != subs.length) {
            // invariant
            return false;
        } else if (subs.length == 0 && arrListsDynamic.length != 0) {
            // invariant
            return false;
        } else if (subs.length > 0 && arrListsDynamic.length % subs.length != 0) {
            // invariant
            return false;
        } else if (arrListsDynamic.length != arrListsSize.length) {
            // invariant
            return false;
        }
        
        uint i;
        uint j;

        self.name = _name;

        for (i = 0; i < subs.length; i++) {
            self.arguments.length += 1;

            self.arguments[i].dataType = ArgumentLib.DataType(dataTypes[i]);
            self.arguments[i].sub = subs[i];
            self.arguments[i].repr = '';
            self.arguments[i].arrList.length = 0;

            for (j = 0; j < arrListsDynamic.length / subs.length; j++) {
                self.arguments[i].arrList.push(ArrayLib.Array({
                    isDynamic: arrListsDynamic[i * subs.length + j],
                    size: arrListsSize[i * subs.length + j],
                    repr: ''
                }));
            }
        }
    }

    function isValid(CanonicalSignature storage self) constant returns (bool) {
        if (bytes(self.name).length == 0) {
            return false;
        } else if (!bytes(self.name)[0].isUnderscore() && !bytes(self.name)[0].isAlpha()) {
            return false;
        } else if (!self.name.isAlphaNumeric()) {
            return false;
        }

        for (uint i = 0; i < self.arguments.length; i++) {
            if (!self.arguments[i].isValid()) {
                return false;
            }
        }

        return true;
    }

    function toString(CanonicalSignature storage self) returns (bool) {
        self.repr = "";
        self.repr.concat(self.name);
        self.repr.concat("(");
        for (uint i = 0; i < self.arguments.length; i++) {
            if (i > 0) {
                self.repr.concat(",");
            }
            self.arguments[i].toString();
            self.repr.concat(self.arguments[i].repr);
        }
        self.repr.concat(")");
        self.selector = bytes4(sha3(self.repr));
        return true;
    }
}
