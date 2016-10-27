pragma solidity ^0.4.0;

import {StringLib} from "contracts/StringLib.sol";


library ArrayLib {
    using StringLib for string;

    struct Array {
        bool isDynamic;
        uint size;
        string repr;
    }

    function isValid(Array storage self) returns (bool) {
        if (self.isDynamic) {
            return self.size == 0;
        } else {
            return true;
        }
    }

    function toString(Array storage self) returns (bool) {
        self.repr = "";
        self.repr.concat("[");
        if (!self.isDynamic) {
            self.repr.concatUInt(self.size);
        }
        self.repr.concat("]");
    }

    function serialize(Array storage self) returns (bool isDynamic,
                                                    uint size) {
        return (self.isDynamic, self.size);
    }
}
