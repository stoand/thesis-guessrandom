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

nodemon -e tex -x 'pdflatex guessrandom.tex && cp guessrandom.pdf /mnt/c/Users/Andreas/Documents/ || echo'

then open `guessrandom.pdf`
