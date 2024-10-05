import argparse

from models import *

# --------------------------- options  --------------------------- #
parser = argparse.ArgumentParser(description="A simple system.")
parser.add_argument(
    "binary",
    default="user/test/sieve/sieve",
    nargs="?",
    type=str,
    help="Path to the binary to execute.",
)
parser.add_argument(
    "--clock_fq", default="1GHz", help=f"System clock frequency."
)
parser.add_argument("--isa", default="X86", help="System ISA.")
parser.add_argument("--l2_size", help="L2 cache size. Default: 256kB.")

options = parser.parse_args()
# --------------------------- options  --------------------------- #

# --------------------------- simulate --------------------------- #
processor = Simple(options)
processor.simulate()
# --------------------------- simulate --------------------------- #
