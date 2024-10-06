import argparse
import subprocess

parser = argparse.ArgumentParser(description="Run gem5 with specified parameters.")

# simulate parameters

parser.add_argument("--isa", nargs="?", default="X86", help="The gem5 build target (e.g., X86, ARM). Default is 'X86'.")
parser.add_argument("--cfg", nargs="?", default="configs/tutorial/simple.py", help="The Python script to run with gem5. Default is 'configs/tutorial/simple.py'.")

# config .py file parameters

parser.add_argument("--bin", default="tests/x86/hello/hello", nargs="?", type=str, help="Path to the binary to execute.")
parser.add_argument("--clk", default="1GHz", nargs="?", type=str, help="Clock frequency. Default is 1GHz")
parser.add_argument("--cpu", default="TimingSimpleCPU", nargs="?", type=str, help="CPU Type. Default is TimingSimpleCPU")
parser.add_argument("--dram", default="DDR3_1600_8x8", nargs="?", type=str, help="DRAM type. Default is DDR3_1600_8x8")
parser.add_argument("additional_args", nargs=argparse.REMAINDER, default=[], help="Additional arguments for the Python script.")

args = parser.parse_args()

# note that the working path for this command depends on the command dir, not the python file dir.
# the working path should also be where you want to generate "m5out" folder.

gem5_command = [
    f"deps/gem5/build/{args.isa}/gem5.opt",
    args.cfg,
    f"--isa={args.isa}",
    f"--bin={args.bin}",
    f"--clk={args.clk}",
    f"--cpu={args.cpu}",
    f"--dram={args.dram}",
    *args.additional_args
]

try:
    subprocess.run(gem5_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running gem5 command: {e}")
