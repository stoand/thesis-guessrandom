# SPC-fpga_mt_rand_verilog
partof: REQ-purpose
###

Use FPGA programmed in Verilog to guess Mersenne Twister random number generator state.

[[.tst-init_next]]

Init the first state after the seed.

[[.tst-init_skip]]

Init the 397th mersenne twister state in a single clock cycle.

## Getting Started

[Buy TinyFPGA BX](https://www.crowdsupply.com/tinyfpga/tinyfpga-bx)

[Install Icestorm](http://www.clifford.at/icestorm)


```
# Don't forget to press reset button before loading program
(cd fpga_mt_rand_verilog/src/; make prog)
```
