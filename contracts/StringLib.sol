pragma solidity ^0.4.0;

import {CharLib} from "contracts/CharLib.sol";


library StringLib {
    using CharLib for bytes1;

    function concat(string storage _head, string tail) returns (bool) {
        bytes head = bytes(_head);

        for (uint i = 0; i < bytes(tail).length; i++) {
            head.push(bytes(tail)[i]);
        }

        _head = string(head);

        return true;
    }

    function concatByte(string storage value, bytes1 b) returns (bool) {
        bytes memory _b = new bytes(1);
        _b[0] = b;
        return concat(value, string(_b));
    }

    function concatUInt(string storage value, uint n) returns (bool) {
        if (n == 0) {
            return concatByte(value, byte(48));
        }
        uint exp;
        if (n >= 10 ** 77) {
            exp = 77;
        } else {
            while (n >= 10 ** (exp + 1)) {
                exp += 1;
            }
        }

        for (uint i = 0; i <= exp; i++) {
            concatByte(value, byte(n / 10 ** (exp - i) + 48));
            n %= 10 ** (exp - i);
        }
        return true;
    }

    function isAlphaNumeric(string value) constant returns (bool) {
        for (uint i = 0; i < bytes(value).length; i++) {
            if (!bytes(value)[i].isAlphaNumeric() && !bytes(value)[i].isUnderscore()) {
                return false;
            }
        }

        return true;
    }
}
