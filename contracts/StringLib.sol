pragma solidity ^0.4.0;

library StringLib {
    function concat(string storage _head, string _tail) returns (bool) {
        bytes head = bytes(_head);
        bytes memory tail = bytes(_tail);

        for (uint i = 0; i < tail.length; i++) {
            head.push(tail[i]);
        }

        _head = string(head);

        return true;
    }

    function concatByte(string storage value, bytes1 b) internal returns (bool) {
        bytes memory _b = new bytes(1);
        _b[0] = b;
        return concat(value, string(_b));
    }

    function concat(string storage value, uint n) returns (bool) {
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
}
