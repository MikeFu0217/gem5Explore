from caches import *

import m5
from m5.objects import *


class Simple:
    def __init__(self, options=None) -> None:
        # binary
        if not options or not options.binary:
            self.binary = "user/test/sieve/sieve"
        else:
            self.binary = options.binary
        # system
        self.system = System()
        # clk
        self.system.clk_domain = SrcClockDomain()
        if not options or not options.clock_fq:
            self.system.clk_domain.clock = "1GHz"
        else:
            self.system.clk_domain.clock = options.clock_fq
        self.system.clk_domain.voltage_domain = VoltageDomain()
        # use timing mode for memory smlation
        self.system.mem_mode = "timing"
        self.system.mem_ranges = [AddrRange("512MB")]
        # cpu
        if not options or not options.isa:
            self.system.cpu = X86TimingSimpleCPU()
        elif options.isa == "X86":
            self.system.cpu = X86TimingSimpleCPU()
        elif options.isa == "RISCV":
            self.system.cpu = RiscvTimingSimpleCPU()
        elif options.isa == "ARM":
            self.system.cpu = ArmTimingSimpleCPU()
        else:
            self.system.cpu = X86TimingSimpleCPU()
        # the system-wide memory bus
        self.system.membus = SystemXBar()
        # simple case without cache connect cpu directly to membus
        self.system.cpu.icache_port = self.system.membus.cpu_side_ports
        self.system.cpu.dcache_port = self.system.membus.cpu_side_ports
        # interrupt
        self.system.cpu.createInterruptController()
        if not options or not options.isa or options.isa == "X86":
            self.system.cpu.interrupts[
                0
            ].pio = self.system.membus.mem_side_ports
            self.system.cpu.interrupts[
                0
            ].int_requestor = self.system.membus.cpu_side_ports
            self.system.cpu.interrupts[
                0
            ].int_responder = self.system.membus.mem_side_ports
        # connect a special port in the system up to the membus
        self.system.system_port = self.system.membus.cpu_side_ports
        # memory controller (simple DDR3)
        self.system.mem_ctrl = MemCtrl()
        self.system.mem_ctrl.dram = DDR3_1600_8x8()
        self.system.mem_ctrl.dram.range = self.system.mem_ranges[0]
        self.system.mem_ctrl.port = self.system.membus.mem_side_ports
        # workload
        self.system.workload = SEWorkload.init_compatible(self.binary)

        self.process = Process()
        self.process.cmd = [self.binary]
        self.system.cpu.workload = self.process
        self.system.cpu.createThreads()

        self.root = Root(full_system=False, system=self.system)
        m5.instantiate()

    def simulate(self):
        print("Beginning simulation!")
        exit_event = m5.simulate()
        print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")


class TwoLevel:
    def __init__(self) -> None:
        self.binary = "tests/test-progs/hello/bin/x86/linux/hello"

        self.system = System()

        self.system.clk_domain = SrcClockDomain()
        self.system.clk_domain.clock = "1GHz"
        self.system.clk_domain.voltage_domain = VoltageDomain()

        self.system.mem_mode = "timing"
        self.system.mem_ranges = [AddrRange("512MB")]

        self.system.cpu = X86TimingSimpleCPU()

        # L1 caches
        self.system.cpu.icache = L1ICache()
        self.system.cpu.dcache = L1DCache()

        self.system.cpu.icache.connectCPU(self.system.cpu)
        self.system.cpu.dcache.connectCPU(self.system.cpu)

        # L2 cache
        self.system.l2bus = L2XBar()
        self.system.cpu.icache.connectBus(self.system.l2bus)
        self.system.cpu.dcache.connectBus(self.system.l2bus)

        self.system.l2cache = L2Cache()
        self.system.l2cache.connectCPUSideBus(self.system.l2bus)
        self.system.membus = SystemXBar()
        self.system.l2cache.connectMemSideBus(self.system.membus)

        # Interruption
        self.system.cpu.createInterruptController()
        self.system.cpu.interrupts[0].pio = self.system.membus.mem_side_ports
        self.system.cpu.interrupts[
            0
        ].int_requestor = self.system.membus.cpu_side_ports
        self.system.cpu.interrupts[
            0
        ].int_responder = self.system.membus.mem_side_ports

        self.system.system_port = self.system.membus.cpu_side_ports

        self.system.mem_ctrl = MemCtrl()
        self.system.mem_ctrl.dram = DDR3_1600_8x8()
        self.system.mem_ctrl.dram.range = self.system.mem_ranges[0]
        self.system.mem_ctrl.port = self.system.membus.mem_side_ports

        self.system.workload = SEWorkload.init_compatible(self.binary)

        self.process = Process()
        self.process.cmd = [self.binary]
        self.system.cpu.workload = self.process
        self.system.cpu.createThreads()

        # instantiate the system and begin execution
        self.root = Root(full_system=False, system=self.system)
        m5.instantiate()

    def simulate(self):
        print("Beginning simulation!")
        self.exit_event = m5.simulate()
        print(
            f"Exiting @ tick {m5.curTick()} because {self.exit_event.getCause()}"
        )
