#SPC-fpga_mt_rand
partof: REQ-purpose
###

Uses FPGA to guess Mersenne Twister random generator state.


## Getting Started

[Buy TinyFPGA BX](https://www.crowdsupply.com/tinyfpga/tinyfpga-bx)

[Install Icestorm](www.clifford.at/icestorm)


Initial Project Setup

```
python3 -m pip install --user virtualenv
python3 -m venv fpga_mt_rand/env

source fpga_mt_rand/env/bin/activate
pip3 install -r fpga_mt_rand/requirements.txt
```

Entering Python Env and Running

```
source fpga_mt_rand/env/bin/activate
# Don't forget to press reset button before loading program
(cd fpga_mt_rand/src/; python3 -m mt_rand)
```

Leaving Python Env

```
deactivate
```
