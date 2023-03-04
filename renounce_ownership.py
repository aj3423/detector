from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

class RenounceOwnership(AbstractDetector):

    ARGUMENT = "RenounceOwnership"  # slither will launch the detector with slither.py --mydetector
    HELP = "check if `Ownable.renounceOwnership()` is overridden and disabled"
    IMPACT = DetectorClassification.LOW
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "see QuillAudits 99Starz (finding A.2)" #TODO: use url instead
    WIKI_TITLE = ARGUMENT
    WIKI_DESCRIPTION = """
Typically, the contract's owner is the account that deploys the contract.
As a result, the owner is able to perform certain privileged activities on
his behalf. The renounceOwnership function is used in smart contracts to
renounce ownership. Otherwise, if the contract's ownership has not been
transferred previously, it will never have an Owner, which is risky.
    """
    WIKI_EXPLOIT_SCENARIO = "..."
    WIKI_RECOMMENDATION = """
It is advised that the Owner cannot call renounceOwnership without first
transferring ownership to a different address. Additionally, if a multi-
signature wallet is utilized, executing the renounceOwnership method
for two or more users should be confirmed. Alternatively, the Renounce
Ownership functionality can be disabled by overriding it.
    """

    def _detect(self):
        results = []

        for contract in self.contracts:  # pylint: disable=too-many-nested-blocks
            if 'Ownable' not in contract.inheritance:
                continue

            if not any(f.full_name == 'renounceOwnership()' for f in contract.functions_declared):
                results.append(self.generate_result(
                    [contract, " `renounceOwnership()` is not overridden and disabled", "\n"]
                ))
        return results

