# SPC-fpga_mt_rand
partof: REQ-purpose
###

Uses FPGA to guess Mersenne Twister random generator state.

[[.tst-simulate]]

Use a nMigen simulation to assert that the Mersenne Twister module
outputs the correct values.

Test style copied from:

[http://blog.lambdaconcept.com/doku.php?id=nmigen:nmigen_sim_testbench](http://blog.lambdaconcept.com/doku.php?id=nmigen:nmigen_sim_testbench)

## Getting Started

[Buy TinyFPGA BX](https://www.crowdsupply.com/tinyfpga/tinyfpga-bx)

[Install Icestorm](http://www.clifford.at/icestorm)


Initial Project Setup

```
npm i -g nodemon

python3 -m pip install --user virtualenv
python3 -m venv fpga_mt_rand/env

source fpga_mt_rand/env/bin/activate
pip3 install -r fpga_mt_rand/requirements.txt
```

Running Tests

```
source fpga_mt_rand/env/bin/activate
(cd fpga_mt_rand/src/; nodemon -e py -x 'python3 -m unittest sim_mt_rand.py || echo')
```

Programming FPGA

```
source fpga_mt_rand/env/bin/activate
# Don't forget to press reset button before loading program
(cd fpga_mt_rand/src/; python3 -m mt_rand)
```

Leaving Python Env

```
deactivate
```

View Logic Cell usage and other Statistics


open `fpga_mt_rand/src/build/top.rpt` and go to end of file
