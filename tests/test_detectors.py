import pytest
import sys
from slither.detectors.abstract_detector import AbstractDetector
from slither.slither import Slither
from detector import plugin_detectors
from typing import Type
from pathlib import Path
from crytic_compile import cryticparser, CryticCompile, InvalidCompilation
import argparse


parser = argparse.ArgumentParser()
# args = parser.parse_known_args()
parser.add_argument('-s', action='store_true')
parser.add_argument('--solc-remaps', type=str, default='')
args = parser.parse_args()

plugin_detectors = plugin_detectors[0:1]
@pytest.mark.parametrize('detector', plugin_detectors)
def test_plugin_detector(detector: Type[AbstractDetector]):
    sol_sample = f'{Path(__file__).resolve().parent}/{detector.__name__}.sol'

    cc = CryticCompile(sol_sample, **vars(args))
    sl = Slither(cc)
    sl.register_detector(detector)
    results = sl.run_detectors()
    
    print(results)
