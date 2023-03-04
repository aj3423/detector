# To make `pytest` not show error:
#  `unrecognized arguments: --solc-remaps`
def pytest_addoption(parser):
    parser.addoption("--solc-remaps") # for finding OpenZeppelin contracts
