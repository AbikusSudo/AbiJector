# setup.py
from setuptools import setup, find_packages

setup(
    name="AbiJector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["psutil"],
    entry_points={
        "console_scripts": [
            "abijector-cli=AbiJector_CLI:main",
            "abijector-gui=AbiJector_GUI:run"
        ]
    },
)
