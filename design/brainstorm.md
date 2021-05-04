# SPC-brainstorm
partof: REQ-purpose
###

# (NOT USED) Pivot Idea - "Onslaught" 

Pivot the project from using old C to 
a project that uses state of the art RNGs.

Automatically provision a couple of FPGAs on Amazon.

# Pivot Idea - Don't use Clash

There isn't a lot of information about the Clash HDL
tool.

The paper should be focused around:

* Challenges / benefits of using FPGAs in general
* Properties of random number generators and breaking them

# Workflow

To pump out 50 pages we have to find fodder for content:

1. Select a Topic (from the list below)
1. (30 min) Find 2-4 books and papers about the respective topic
2. (8 hours) Read 50-200 pages
3. (2 hours) Write ~5-8 pages about the topic

# Topic List

Fodder Topics with (Page count)

FPGAs

* (5) FPGA business applications / general background
* (5) FPGA internal architecture
* (5) FPGA varieties on the market / vendors / toolchains / open source

RNGs

* (5) Random number generator basics
* (5) History of RNG Implentations back to ancient times
* (5) Entropy - Mathematical Theory 
* (5) Real life examples of RNG exploits
* (5) Stats comparing RNG attacks to other types of exploits
    or why RNG attacks are not more popular

Marriage of the Two, Our Project Itself

* (1) Introduction
* (5) Verilog Implementation + testing
* (5) Conclusion / Possible Future Experiments / Improvements
