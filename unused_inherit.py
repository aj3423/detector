from slither.core.declarations import Function, Contract, Modifier, Event
from slither.core.variables.state_variable import StateVariable
from slither.slithir.operations import InternalCall, EventCall


from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification


def to_name_set(lst):
    return {x.canonical_name for x in lst}

class UnusedInherit(AbstractDetector):

    ARGUMENT = "UnusedInherit"  # slither will launch the detector with slither.py --mydetector
    HELP = "Inherits from a contract but never uses any function of it"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "quill Acknoledger (A.3)"
    WIKI_TITLE = ARGUMENT
    WIKI_DESCRIPTION = HELP
    WIKI_EXPLOIT_SCENARIO = "..."
    WIKI_RECOMMENDATION = HELP


    @staticmethod
    def list_things_used_by_contract(contract : Contract, func_list = None):
        """
        return tuple(variable[], function[], modifier[]): 
          all the variable/functions used by this contract's own functions and modifiers)
        """
        vars  = set['StateVariable']()
        funcs = set['Function']()
        mods = set['Modifier']()
        evts = set['EventCall']()

        if func_list is None:
            func_list = contract.functions_declared + contract.modifiers

        for f in func_list: # include func/mod
            mods |= set(f.modifiers)

            for n in f.nodes:
                vars |= set(n.state_variables_read)
                vars |= set(n.state_variables_written)

                for ir in n.irs:
                    if isinstance(ir, (EventCall)):
                        evts.add(ir)
                    if isinstance(ir, (InternalCall)) and not ir.is_modifier_call: #modiriers are handled seperately with `mods`
                        if ir.function:
                            funcs.add(ir.function)
        return vars, funcs, mods, evts


    def _detect(self):
        results = []

        for contract in self.compilation_unit.contracts:
            # print('\n---', contract.name)

            var_used, func_used, mod_used, evt_used = self.list_things_used_by_contract(contract)

            
            var_name_used  = to_name_set(var_used)
            func_name_used = to_name_set(func_used)
            mod_name_used  = to_name_set(mod_used)
            evt_name_used  = {x.name for x in evt_used} # `EventCall` only has `name`, no `canonical_name` available

            for inherit in contract.immediate_inheritance:

                # all var/func/mod declared in inherited contract
                inh_var_name  = to_name_set(inherit.state_variables_declared)
                inh_func_name = to_name_set(inherit.functions_declared)
                inh_mod_name  = to_name_set(inherit.modifiers_declared)
                inh_evt_name  = {x.name for x in inherit.events_declared}

                if (
                    inherit.constructors_declared # parent has a construct which will always be called
                    or var_name_used  & inh_var_name # any parent variable used?
                    or func_name_used & inh_func_name # any parent function used?
                    or mod_name_used  & inh_mod_name # any parent modifier used?
                    or evt_name_used  & inh_evt_name # any parent event used?
                ):
                    continue
                
                res = self.generate_result(
                    "Unused Inherit: <%s> inherits from <%s> but not used, should be removed\n" 
                    % (contract.name, inherit.name)
                )
                results.append(res)
        
        return results
