# SPC-fpga_lcg
partof: REQ-purpose
###

__DANGER: writing to the wrong location in ram can CORRUPT THE BOOTLOADER. See `tinyprog -m` for memory ranges.__


Verilog implementation on functional language evaluation engine.

## Getting Started

[Buy TinyFPGA BX](https://www.crowdsupply.com/tinyfpga/tinyfpga-bx)

[Install Icestorm](http://www.clifford.at/icestorm)

[Setup Symbiyosys](https://symbiyosys.readthedocs.io/en/latest/quickstart.html)


## Simulation

```
make reduce.sim-watch
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

### Links

[TinyFPGA_BX guide](http://www.latticesemi.com/~/media/LatticeSemi/Documents/DataSheets/iCE/iCE40LPHXFamilyDataSheet.pdf)

[TinyFPGA_BX memory guide](http://www.latticesemi.com/-/media/LatticeSemi/Documents/ApplicationNotes/MO/MemoryUsageGuideforiCE40Devices.ashx?document_id=47775)

[ultimate calculus](https://github.com/MaiaVictor/ultimate-calculus)

[abstract calculus blog post](https://medium.com/@maiavictor/the-abstract-calculus-fe8c46bcf39c)

[symmetric interaction calculus](https://github.com/MaiaVictor/Symmetric-Interaction-Calculus)

[Elementary Affine Logic](https://github.com/MaiaVictor/Elementary-Affine-Core-legacy/blob/master/spec.md)
