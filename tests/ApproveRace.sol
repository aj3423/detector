// SPDX-License-Identifier: MIT
pragma solidity ^ 0.8.0;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ApproveRace is ERC20("", "") {

	function approve(address spender, uint256 amount) public virtual override returns (bool) {
		// allowance(_msgSender(), spender);
		_approve(_msgSender(), spender, amount);
		return true;
	}
}

