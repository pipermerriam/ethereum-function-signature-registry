pragma solidity ^0.4.0;


contract owned {
    address public owner;

    function owned() {
        owner = msg.sender;
    }

    modifier onlyowner {
        if (msg.sender != owner) {
            throw;
        } else {
            _;
        }
    }

    event OwnerChanged(address indexed oldOwner, address indexed newOwner);

    function transferOwner(address newOwner) public onlyowner returns (bool) {
        OwnerChanged(owner, newOwner);
        owner = newOwner;
        return true;
    }
}
