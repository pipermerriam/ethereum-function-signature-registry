pragma solidity ^0.4.0;


library CharLib {
    function isUnderscore(bytes1 v) returns (bool) {
        return v == '_';
    }

    function isAlphaUpper(bytes1 v) returns (bool) {
        return (uint(v) >= uint(bytes1('A')) && uint(v) <= uint(bytes1('Z')));
    }

    function isAlphaLower(bytes1 v) returns (bool) {
        return (uint(v) >= uint(bytes1('a')) && uint(v) <= uint(bytes1('z')));
    }

    function isDigit(bytes1 v) returns (bool) {
        return (uint(v) >= uint(bytes1('0')) && uint(v) <= uint(bytes1('9')));
    }

    function isAlpha(bytes1 v) returns (bool) {
        return (isAlphaUpper(v) || isAlphaLower(v));
    }

    function isAlphaNumeric(bytes1 v) returns (bool) {
        return (isAlpha(v) || isDigit(v) );
    }
}
