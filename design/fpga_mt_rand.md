# SPC-fpga_mt_rand
partof: REQ-purpose
###

Uses FPGA to guess Mersenne Twister random generator state.

[[.tst-simulate]]

Use a nMigen simulation to assert that the Mersenne Twister module
outputs the correct values.

Test style copied from:

[http://blog.lambdaconcept.com/doku.php?id=nmigen:nmigen_sim_testbench](http://blog.lambdaconcept.com/doku.php?id=nmigen:nmigen_sim_testbench)


[[.tst-fast_multiplication]]

Multiplication is by far the most expensive operation in the Mersenne Twister algorithm.

This can be checked by adding an algorithm with (say 10) multiplications and checking the logic cell statistics.

Therefore, an optimization mentioned in the post below needs to be applied to make initializing hundreds

of Mersenne Twister states in a single clock cycle viable.

[Blog post with various multiplication optimizations](http://www.andraka.com/multipli.php)


[[.tst-deeply_nested_operators]]

Currently, performing an algorithm around 10 times on a single signal, slows down
compilation time to a few dozen seconds.

However, algorithms that are nested 100 times or more and applied to a single signal result in a stack error.

To fix this, the algorithm used by _nmigen_ needs to be optimized to allow for deeply nested operators.


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


Timing Analysis


```
icetime fpga_mt_rand/src/build/top.asc
```
