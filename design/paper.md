# SPC-paper
partof: REQ-purpose
###

The design was modeled after the paper "Monotonic Aggregation in Deductive Databases". 

## Title of the Paper

Novel use of a Functional HDL to simplify development of a RNG Brute-Force Algorithm

## Building the Latex Paper

```
sudo apt install texlive-latex-recommended texlive-pictures texlive-latex-extra texlive-fonts-extra

pdflatex guessrandom.tex

# Or watch
npm i -g nodemon
nodemon -e tex -x 'pdflatex guessrandom.tex || echo'
```

```
nodemon -e tex -x '(pdflatex guessrandom.tex || echo) && sleep 0.1 && cp guessrandom.pdf /mnt/c/Users/Andreas/Documents/ || echo'
```

then open `guessrandom.pdf`

## Professor Feedback

See `./change_annotations_1.pdf`.

Also:

```
Please find attached my comments. Overall, it is a very good project.

I added some notes. Please take a look at the note in section 5, suggesting
the addition of section 5.4

What is missing, I think, is explicitly stating the motivation and importance of the work.
So, by adding 5.4, one could realize then motivation…Also, it is important to state in section 6
how many bits are the typical RNG…Also, how your FPGA design is going to change to break a 64-bit RNG?

Please let me know if you have any questions on the above. Your presentation is scheduled for June 7, so if you could get your committee members the final draft by June 4 that will be great! 
```

Changes:

Section 5.5: added

Section 7:

Paragraph: "Just this brute force approach" ...

## Presentation Reviewer Feedback

GPU Comparison - Section 2, "FPGAs are also frequently compared to GPUs."

Serious (PHP) RNG info/demonstration

ASIC vs FPGA comparison table - Section 2 table

Move running stats to section 7

Proper template

More description of Verilog source

## Advisor Feedback

1. How difficult will it be to make your code also run for a 64-bit RNG?

In a sense, how difficult will it be to set a flag to determine whether we are
running for a 32-bit RNG or for a 64-bit one?

2. Could you give a rough estimate how long it will take to compromise a 64-bit RNG?

We are thinking to extend your work by addressing the above! And in addition, run the code on a GPU and compare\contrast the findings. Needless to say, you are done with your FYP :) We will get another student to continue — unless you do an MSc and that will be your thesis! :) 

