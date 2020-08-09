# SPC-paper
partof: REQ-purpose
###

The design was modeled after the paper "Monotonic Aggregation in Deductive Databases". 

## Building the Latex Paper

```
sudo apt install texlive-latex-recommended texlive-pictures texlive-latex-extra texlive-fonts-extra

pdflatex guessrandom.tex

# Or watch
npm i -g nodemon
nodemon -e tex -x 'pdflatex guessrandom.tex || echo'
```

then open `guessrandom.pdf`
