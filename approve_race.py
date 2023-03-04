from collections import namedtuple, defaultdict
from typing import Dict, Set, List

from slither.detectors.abstract_detector import DetectorClassification, AbstractDetector
from slither.utils.output import Output


class ApproveRace(AbstractDetector):
    ARGUMENT = "ApproveRace"
    HELP = "ERC20 Approve Race"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = (
        "https://swcregistry.io/docs/SWC-114"
    )

    WIKI_TITLE = HELP

    # region wiki_description
    WIKI_DESCRIPTION = """
Approval change can lead to two transactions, should approve 0 first or use increase/decrease of allowance instead.
"""
    # endregion wiki_description

    # region wiki_exploit_scenario
    WIKI_EXPLOIT_SCENARIO = """
```solidity
    1. monitor new approval, send TX with amount==old_approval using higher gas
    2. send TX2 with amount == new approval
```
"""
    # endregion wiki_exploit_scenario

    WIKI_RECOMMENDATION = "Only allow `approve()` if current approval is 0 or use increase/decrease of allowance instead"

    STANDARD_JSON = False


    def _detect(self) -> List[Output]:  # pylint: disable=too-many-branches

        results = []

        for contract in self.contracts:  # pylint: disable=too-many-nested-blocks
            # only detect if `Contract is ERC20`
            if not contract.is_erc20():
                continue
            if 'ERC20' not in contract.inheritance:
                continue

            for f in contract.functions_declared:
                if f.name != 'approve':
                    continue

                #if it get current allowance, it may use 
                # increase/decrease allowance` instead,
                # or check if it's 0
                has_allowance_access = False

                for node in f.nodes:
                    for ir in node.irs:
                        if ir.function.canonical_name in [
                            'ERC20.allowance(address,address)', 
                            'ERC20.increaseAllowance(address,uint256)', 
                            'ERC20.decreaseAllowance(address,uint256)'
                        ]:
                            has_allowance_access = True

                        if ir.function.canonical_name == 'ERC20._approve(address,address,uint256)' and not has_allowance_access:
                            results.append(self.generate_result(
                                ["approve() race in", f, ":\n"]
                            ))


        return results
