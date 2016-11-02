pragma solidity ^0.4.0;

import {owned} from "./owned.sol";


contract authorized is owned {
    mapping (address => bool) authorized;

    modifier auth {
        if (!authorized[msg.sender]) {
            throw;
        } else {
            _;
        }
    }

    event AuthorizationAdded(address indexed _who);
    event AuthorizationRemoved(address indexed _who);

    function addAuthorization(address _who) public onlyowner returns (bool) {
        if (authorized[_who]) return false;

        authorized[_who] = true;
        AuthorizationAdded(_who);

        return true;
    }

    function removeAuthorization(address _who) public onlyowner returns (bool) {
        if (!authorized[_who]) return false;

        authorized[_who] = false;
        AuthorizationRemoved(_who);

        return true;
    }
}
