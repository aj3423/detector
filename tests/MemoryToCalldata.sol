// SPDX-License-Identifier: MIT
pragma solidity ^ 0.8.0;

contract MemoryToCalldata {
	function test_memory(uint[1] memory a, uint[1] memory) public pure returns (uint) {
		return a[0];
	}
	function test_memory2(uint[1] memory a, uint[1] memory) public pure returns (uint) {
		a[0] = 1;
		return a[0];
	}
	function test_calldata(uint[1] calldata a, uint[1] calldata) public pure returns (uint) {
		return a[0];
	}

	// for testing old compiler version(<0.8)
	// `public` should optimized to `external` if not referenced
	function public_function() public {}

	function private_function() private {
		public_function();
	}
	function internal_function() internal {
		public_function();
	}
}

