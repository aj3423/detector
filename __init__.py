from approve_race import ApproveRace
from renounce_ownership import RenounceOwnership
from memory_to_calldata import MemoryToCalldata
from unused_inherit import UnusedInherit

plugin_detectors = [
    ApproveRace, 
    RenounceOwnership,
    MemoryToCalldata,
    UnusedInherit
]

def make_plugin():
    plugin_printers = []

    return plugin_detectors, plugin_printers
