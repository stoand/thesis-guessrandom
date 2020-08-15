# Notes


# Previous Work

## Breaking Mersenne Twister without bruteforce

[Blog post](https://www.ambionics.io/blog/php-mt-rand-prediction)

Limitations: 
* Requires outputs exactly 262 cycles apart
* Requires a large number of outputs

Benefits
* Requires an order of magnitude less computation

## Untwister

[Github Repository](https://github.com/bishopfox/untwister)

Limitations
* Requires a huge amount of computation - on the order of hours

Benefits
* More versatile
* Requires fewer observed outputs

## Mersenne Twister Random Number Generation on FPGA, CPU and GPU

[Paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1058.1244&rep=rep1&type=pdf)

Shows that the FPGA is an order of magnitude faster and more energy efficient at computing outputs.


## High Performance FPGA implementation of the Mersenne Twister

[Paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.426.2658&rep=rep1&type=pdf)

Limitations
* Used costly, inaccessable hardware (though it might be economical to rent through the cloud)

Benefits
* Incredibly high throughput - 22 Million Outputs / Second


