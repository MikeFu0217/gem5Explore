# Gem5 Explore

To run this project, clone this repository under the same directory of gem5. (shoulder-by-shoulder)

## Run sim_simple.py with variable configurations

Run the following command to see available options:

```
$ python sim_simple.py --help
```

You shall see:

```
usage: sim_simple.py [-h] [--isa [ISA]] [--cfg [CFG]] [--bin [BIN]] [--clk [CLK]] [--cpu [CPU]] [--dram [DRAM]] ...

Run gem5 with specified parameters.

positional arguments:
  additional_args  Additional arguments for the Python script.

options:
  -h, --help       show this help message and exit
  --isa [ISA]      The gem5 build target (e.g., X86, ARM). Default is 'X86'.
  --cfg [CFG]      The Python script to run with gem5. Default is 'configs/tutorial/simple.py'.
  --bin [BIN]      Path to the binary to execute.
  --clk [CLK]      Clock frequency. Default is 1GHz
  --cpu [CPU]      CPU Type. Default is TimingSimpleCPU
  --dram [DRAM]    DRAM type. Default is DDR3_1600_8x8
```

A more detailed explanation on options:
- `--isa`: Set the simulator ISA and the corresponding CPU. You should have built the ISA in your gem5. Binary file should correspond to your ISA.
- `--cfg`: Choose the path of the script to run. Path can be relative to your current command line path, or absolute path. Config file should be carefully written to reveice parameters from sim_simple.py.
- `--bin`: Choose binary file to execute. This file should coorespond to your ISA. Used in script as `system.workload = SEWorkload.init_compatible([bin])` and `process.cmd = [[bin]]`.
- `--clk`: Clock frequency. Used in script as `system.clk_domain.clock = [clk]`. You can choose like "1GHz", "3GHz" and so on.
- `--cpu`: Choose from CPU Models supported by gem5. Used in script as `system.cpu = [cpu]`. Options contain: "TimingSimpleCPU" "MinorCPU" "O3CPU"...
- `--dram`: Choose from dram support by gem5. Used in script as `system.mem_ctrl.dram = [dram]`.