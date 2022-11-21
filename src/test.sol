// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.8;

contract TestContract {
    uint256 a = 100;
    uint256 b = 0;
    function deal(uint256 number) public {
        a = a - number;
        b = b + number;
    }
}
