pragma solidity ^0.4.0;

import {ArrayLib} from "contracts/ArrayLib.sol";


contract TestArrayLib {
    using ArrayLib for ArrayLib.Array;

    ArrayLib.Array value;

    function repr() constant returns (string) {
        return value.repr;
    }

    function set(bool isDynamic, uint size) public returns (bool) {
        value.isDynamic = isDynamic;
        value.size = size;
        value.toString();
        return true;
    }
}
