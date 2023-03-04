from slither.core.solidity_types import ArrayType, MappingType
from slither.core.variables.local_variable import LocalVariable
from slither.core.solidity_types import UserDefinedType
from slither.core.declarations.structure import Structure
from slither.core.solidity_types.array_type import ArrayType

from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

class MemoryToCalldata(AbstractDetector):

    ARGUMENT = "MemoryToCalldata"  # slither will launch the detector with slither.py --mydetector
    HELP = "`memory` -> `calldata` if an argument is not mutated within the function"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://ethereum.stackexchange.com/a/89999/75827"
    WIKI_TITLE = ARGUMENT
    WIKI_DESCRIPTION = """
For new solc version(>=0.8), it's now `memory` and `calldata` that matters:
    - `calldata`: cheap, readonly
    - `memory`: need extra allocation

For old solc version(<0.8), it's `public` and `external`
    - `public` maybe called by internal function, reference types of variables 
        are copied to memory first, which costs more gas.
    - `external` doesn't copy variables, saves gas and more performant.
    """
    WIKI_EXPLOIT_SCENARIO = "..."
    WIKI_RECOMMENDATION = HELP

    @staticmethod
    def is_reference_type(parameter: LocalVariable) -> bool:
        parameter_type = parameter.type
        if isinstance(parameter_type, ArrayType):
            return True
        if isinstance(parameter_type, UserDefinedType) and isinstance(
            parameter_type.type, Structure
        ):
            return True
        if str(parameter_type) in ["bytes", "string"]:
            return True
        return False


    def _detect(self):
        results = []
        # if need version check, see: slither's 'incorrect_solc.py'

        for contract in self.compilation_unit.contracts_derived:
            for f in contract.functions_entry_points: # public/external only

                args = [a for a in f.parameters if a.location == 'memory' and self.is_reference_type(a)]
                if len(args) == 0: # no 'memory' args
                    continue

                for node in f.nodes:
                    for ir in node.irs:
                        args = list(filter(lambda a: 
                            a not in ir.node.local_variables_written,
                        args))

                for arg in args:
                    results.append(self.generate_result(
                        ["'", arg.canonical_name, "' can be optimized from `memory` to `calldata` to save gas", "\n"]
                    ))
        return results

