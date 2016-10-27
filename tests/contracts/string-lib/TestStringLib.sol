pragma solidity ^0.4.0;

import {StringLib} from 'contracts/StringLib.sol';


contract TestStringLib {
    using StringLib for string;

    string public value;

    function reset() public returns (bool) {
        value = "";
        return true;
    }

    function set(string v) public returns (bool) {
        value = v;
        return true;
    }

    function concatString(string tail) public returns (bool) {
        return value.concat(tail);
    }

    function concatUInt(uint v) public returns (bool) {
        return value.concatUInt(v);
    }
}
