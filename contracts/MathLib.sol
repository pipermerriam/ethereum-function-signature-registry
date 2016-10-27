pragma solidity ^0.4.0;


library MathLib {
    function sum(uint[] values) constant returns (uint total) {
        for (uint i = 0; i < values.length; i++) {
            total += values[i];
        }
        return total;
    }
}
