# AbiJector_CLI.py
import argparse
from AbiJector_LIB import AbiJector

parser = argparse.ArgumentParser(description="AbiJector CLI — DLL injector")
parser.add_argument("--process", required=True, help="Target process name (e.g., Dungeons.exe)")
parser.add_argument("--dll", required=True, help="Path to the DLL file")
args = parser.parse_args()

injector = AbiJector(args.process, args.dll)
injector.inject()