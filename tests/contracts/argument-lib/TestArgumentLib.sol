pragma solidity ^0.4.0;

import {ArgumentLib} from "contracts/ArgumentLib.sol";
import {ArrayLib} from "contracts/ArrayLib.sol";


contract TestArgumentLib {
    using ArgumentLib for ArgumentLib.Argument;

    ArgumentLib.Argument value;

    function repr() constant returns (string) {
        return value.repr;
    }

    function reset() public returns (bool) {
        value.dataType = ArgumentLib.DataType(0);
        value.sub = 0;
        value.arrList.length = 0;
        value.repr = "";
    }

    function set(uint dataType,
                 uint sub,
                 bool[] arrListDynamic,
                 uint[] arrListSize) public returns (bool) {
        if (arrListDynamic.length != arrListSize.length) {
            // invariant
            throw;
        }
        value.dataType = ArgumentLib.DataType(dataType);
        value.sub = sub;
        value.arrList.length = 0;

        for (uint i = 0; i < arrListDynamic.length; i++) {
            value.arrList.push(ArrayLib.Array({
                isDynamic: arrListDynamic[i],
                size: arrListSize[i],
                repr: ""
            }));
        }
        if (value.isValid()) {
            value.toString();
        }
        return true;
    }

    function isValid() constant returns (bool) {
        return value.isValid();
    }
}
