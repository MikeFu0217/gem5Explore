import m5
from m5.objects import *

import sys
import argparse

# --------------------------- options ---------------------------#
parser = argparse.ArgumentParser(description="A simple system with Timing Simple CPU.")
parser.add_argument("--isa", default="X86", nargs="?", type=str, help="Instruction set architecture. Choose from what you have built. Default is X86")
parser.add_argument("--bin", default="tests/x86/hello/hello", nargs="?", type=str, help="Path to the binary to execute.")
parser.add_argument("--clk", default="1GHz", nargs="?", type=str, help="Clock frequency. Default is 1GHz")
parser.add_argument("--cpu", default="TimingSimpleCPU", nargs="?", type=str, help="CPU Type. Default is TimingSimpleCPU")
parser.add_argument("--dram", default="DDR3_1600_8x8", nargs="?", type=str, help="DRAM type. Default is DDR3_1600_8x8")
options = parser.parse_args()
# --------------------------- options ---------------------------#

# The System object will be the parent of all the other objects in our simulated system.
# The System object contains a lot of functional (not timing level) information,
# like the physical memory ranges, the root clock domain, the root voltage domain, the kernel (in full-system simulation), etc.

system = System()

# Set the clock on the system

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = options.clk
system.clk_domain.voltage_domain = VoltageDomain()

# We are going to use timing mode for the memory simulation.
# You will almost always use timing mode for the memory simulation,
# except in special cases like fast-forwarding and restoring from a checkpoint.
# We will also set up a single memory range of size 512 MB,a very small system.

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# We will start with the most simple timing-based CPU in gem5 for the X86 ISA, X86TimingSimpleCPU.
# This CPU model executes each instruction in a single clock cycle to execute, except memory requests, which flow through the memory system.

cpuName = f"{options.isa}".capitalize() + f"{options.cpu}"
system.cpu = globals()[cpuName]()

# the system-wide memory bus

system.membus = SystemXBar()

# Now that we have a memory bus, let’s connect the cache ports on the CPU to it.
# In this case, since the system we want to simulate doesn’t have any caches,
# we will connect the I-cache and D-cache ports directly to the membus. In this example system, we have no caches.

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# Connecting the PIO and interrupt ports to the memory bus is an x86-specific requirement.
# Other ISAs (e.g., ARM) do not require these 3 extra lines.

system.cpu.createInterruptController()
if options.isa == "X86":
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

# create a memory controller and connect it to the membus.
# For this system, we’ll use a simple DDR3 controller and it will be responsible for the entire memory range of our system.

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = globals()[f"{options.dram}"]()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Create the process (another SimObject).
# Then we set the processes command to the command we want to run.
# Then we set the CPU to use the process as it’s workload, and finally create the functional execution contexts in the CPU.

binary = options.bin
#binary = "/home/zuoming/projects/gem5/gem5Explore/tests/sieve/sieve"

system.workload = SEWorkload.init_compatible(binary)  # for gem5 V21 and beyond

process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# instantiate the system and begin execution
root = Root(full_system=False, system=system)
m5.instantiate()

# kick off the actual simulation

print("Beginning simulation!")
exit_event = m5.simulate()

# once simulation finishes, we can inspect the state of the system.

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
