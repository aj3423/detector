// SPDX-License-Identifier: MIT
pragma solidity ^ 0.8.0;

// import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

// contract Base is Ownable{
contract Base {
	event evBase();

	uint bas;
}

// `is Base` should be optimized
contract Middle is Base {
	uint mid; 

	modifier midMod() {
		_;
	}
	function midFunc() public {
		// emit evBase();
	}
}

// `is Middle` is ok
contract Test is Middle {
	uint tst;

	modifier testMod() {
		midFunc();
		_;
	}
	function testMemory() midMod external view returns (uint) {
		return tst + mid;
	}
}
