// SPDX-License-Identifier: Unlicense
pragma solidity >=0.8.0;
import "forge-std/Test.sol";

contract Cheat is Test {
    Vm vm = Vm(0x7109709ECfa91a80626fF3989D68f67F5b1DD12D);
    
    function Deal(address addr, uint256 amount) public {
        vm.deal(addr, amount);
    }
}
