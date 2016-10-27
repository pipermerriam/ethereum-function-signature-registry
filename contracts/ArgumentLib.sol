pragma solidity ^0.4.0;

import {StringLib} from "contracts/StringLib.sol";
import {ArrayLib} from "contracts/ArrayLib.sol";


library ArgumentLib {
    using StringLib for string;
    using ArrayLib for ArrayLib.Array;

    enum DataType {
        Null,
        Address,
        Bool,
        UInt,
        Int,
        BytesFixed,
        BytesDynamic,
        String
    }

    struct Argument {
        DataType dataType;
        uint sub;
        ArrayLib.Array[] arrList;
        string repr;
    }

    function serialize(Argument storage self) returns (uint dataType,
                                                       uint sub) {
        return (uint(self.dataType), self.sub);
    }

    function toString(Argument storage self) returns (bool) {
        if (!isValid(self)) {
            return false;
        }

        self.repr = "";

        if (self.dataType == DataType.Address) {
            self.repr.concat('address');
        } else if (self.dataType == DataType.Bool) {
            self.repr.concat('bool');
        } else if (self.dataType == DataType.UInt) {
            self.repr.concat('uint');
            self.repr.concatUInt(self.sub);
        } else if (self.dataType == DataType.Int) {
            self.repr.concat('int');
            self.repr.concatUInt(self.sub);
        } else if (self.dataType == DataType.BytesFixed) {
            self.repr.concat('bytes');
            self.repr.concatUInt(self.sub);
        } else if (self.dataType == DataType.BytesDynamic) {
            self.repr.concat('bytes');
        } else if (self.dataType == DataType.String) {
            self.repr.concat('string');
        }

        for (uint i = 0; i < self.arrList.length; i++) {
            self.arrList[i].toString();
            self.repr.concat(self.arrList[i].repr);
        }

        return true;
    }

    function isValid(Argument storage self) constant returns (bool) {
        for (uint i = 0; i < self.arrList.length; i++) {
            if (!self.arrList[i].isValid()) {
                return false;
            }
        }

        if (self.dataType == DataType.Address) {
            return validateAddress(self);
        } else if (self.dataType == DataType.Bool) {
            return validateBool(self);
        } else if (self.dataType == DataType.UInt) {
            return validateUInt(self);
        } else if (self.dataType == DataType.Int) {
            return validateInt(self);
        } else if (self.dataType == DataType.BytesFixed) {
            return validateBytesFixed(self);
        } else if (self.dataType == DataType.BytesDynamic) {
            return validateBytesDynamic(self);
        } else if (self.dataType == DataType.String) {
            return validateString(self);
        } else {
            // shouldn't be possible
            throw;
        }
    }

    function validateAddress(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.Address) {
            return false;
        } else if (self.sub != 0) {
            return false;
        } else {
            return true;
        }
    }

    function validateBool(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.Bool) {
            return false;
        } else if (self.sub != 0) {
            return false;
        } else {
            return true;
        }
    }

    function validateUInt(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.UInt) {
            return false;
        } else if (self.sub > 256) {
            return false;
        } else if (self.sub < 8) {
            return false;
        } else if (self.sub % 8 != 0) {
            return false;
        } else {
            return true;
        }
    }

    function validateInt(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.Int) {
            return false;
        } else if (self.sub > 256) {
            return false;
        } else if (self.sub < 8) {
            return false;
        } else if (self.sub % 8 != 0) {
            return false;
        } else {
            return true;
        }
    }

    function validateBytesFixed(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.BytesFixed) {
            return false;
        } else if (self.sub > 32) {
            return false;
        } else if (self.sub < 1) {
            return false;
        } else {
            return true;
        }
    }

    function validateBytesDynamic(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.BytesDynamic) {
            return false;
        } else if (self.sub != 0) {
            return false;
        } else {
            return true;
        }
    }

    function validateString(Argument storage self) internal returns (bool) {
        if (self.dataType != DataType.String) {
            return false;
        } else if (self.sub != 0) {
            return false;
        } else {
            return true;
        }
    }
}
