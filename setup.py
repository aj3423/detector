from setuptools import setup, find_packages

setup(
    name="detector",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["slither-analyzer>0.1"],
    entry_points={
        "slither_analyzer.plugin": "slither my-plugin=detector:make_plugin",
    },
)
