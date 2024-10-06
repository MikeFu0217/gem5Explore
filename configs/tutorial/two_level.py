import argparse

from caches import *  # import the names from the caches.py file into the namespace

import m5
from m5.objects import *

# --------------------------- options ---------------------------#
parser = argparse.ArgumentParser(description="A simple system with Timing Simple CPU.")
parser.add_argument("--isa", default="X86", nargs="?", type=str, help="Instruction set architecture. Choose from what you have built. Default is X86")
parser.add_argument("--bin", default="tests/x86/hello/hello", nargs="?", type=str, help="Path to the binary to execute.")
parser.add_argument("--clk", default="1GHz", nargs="?", type=str, help="Clock frequency. Default is 1GHz")
parser.add_argument("--cpu", default="TimingSimpleCPU", nargs="?", type=str, help="CPU Type. Default is TimingSimpleCPU")
parser.add_argument("--dram", default="DDR3_1600_8x8", nargs="?", type=str, help="DRAM type. Default is DDR3_1600_8x8")
parser.add_argument("--l1i_size", help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", help="L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l2_size", help="L2 cache size. Default: 256kB.")
options = parser.parse_args()
# --------------------------- options ---------------------------#

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = options.clk
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# cpu
cpuName = f"{options.isa}".capitalize() + f"{options.cpu}"
system.cpu = globals()[cpuName]()

# create L1 caches
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

# connect the caches to the CPU ports with the helper function we created.

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# create an L2 bus to connect our L1 caches to the L2 cache

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# create our L2 cache and connect it to the L2 bus and the memory bus

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
if options.isa == "X86":
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = globals()[f"{options.dram}"]()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(
    options.bin
)  # for gem5 V21 and beyond

process = Process()
process.cmd = [options.bin]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
