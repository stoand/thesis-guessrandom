# SPC-fpga_lcg
partof: REQ-purpose
###

Verilog implementation of a brute for program for a  Linear Congruential Random Number Generator.

__DANGER: writing to the wrong location in ram can CORRUPT THE BOOTLOADER. See `tinyprog -m` for memory ranges.__


## Getting Started

[Buy TinyFPGA BX](https://www.crowdsupply.com/tinyfpga/tinyfpga-bx)

[Install Icestorm](http://www.clifford.at/icestorm)

[Setup Symbiyosys](https://symbiyosys.readthedocs.io/en/latest/quickstart.html)


## Simulation

```
make lcg.sim

make lcg.sim-watch
```

## Programming the FPGA

```
# Don't forget to press the reset button before programming
make lcg.prog
```

## Programming the FPGA while inside Windows Subsystem for Linux 2 (WSL2)

Setup:
* Install Python with update path enabled
* in powershell: `pip install tinyprog`

Programming:

```
# Don't forget to press the reset button before programming
make lcg.prog-wsl2
```

## Viewing Logic Cell Usage

```
make build/lcg.json

<editor> build/lcg.log
```

## Generate a clock with a given frequency

`icepll -i 16 -o 50 -m -f 50mhz.v`

Replace '50' with the desired clock speed.

## Tests

__To view variable values:__

Ensure an assertion fails then:

open `build/lcg/engine_0/trace.vcd`

## 32/64 Bit Configuration

To modify `SIZE` in simulations:

Edit `read -define SIZE=...` in [./fpga_lcg/lcg.sby](../fpga_lcg/lcg.sby).


To modify `SIZE` when programming FPGA:

Edit `yosys -D SIZE=...` in [./fpga_lcg/Makefile](../fpga_lcg/Makefile)

_Note: set `SIZE` to 31 and 63 bits (not 32 and 64)_


### Links

[TinyFPGA_BX guide](http://www.latticesemi.com/~/media/LatticeSemi/Documents/DataSheets/iCE/iCE40LPHXFamilyDataSheet.pdf)

[TinyFPGA_BX memory guide](http://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/MO/MemoryUsageGuideforiCE40Devices.ashx?document_id=47775)
