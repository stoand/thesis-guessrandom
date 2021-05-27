# SPC-present
partof: REQ-purpose
###

Create a "Beamer" presentation.

Follow this tutorial:

https://www.overleaf.com/learn/latex/Beamer_Presentations:_A_Tutorial_for_Beginners_(Part_1)%E2%80%94Getting_Started

## Presentation Info

```
Your FYP presentation has been scheduled and the zoom link has been sent to you already.

Please note that the presentation (in ppt) will be 10-15 minutes,
followed by 5-10 minutes demonstration of the program, if any.

The overall presentation must be concluded in 20 minutes, so please plan accordingly. 

Make sure to send to your committee members your report (in pdf please) a
few days before your presentation (3-4 days).
```

## Themes

https://github.com/martinbjeldbak/ultimate-beamer-theme-list

## Building the Beamer Latex Presentation

```
sudo apt install texlive-latex-recommended texlive-pictures texlive-latex-extra texlive-fonts-extra

pdflatex present.tex

# Or watch
npm i -g nodemon
nodemon -e tex -x 'pdflatex present.tex || echo'
```

```
nodemon -e tex -x '(pdflatex present.tex || echo) && cp present.pdf /mnt/c/Users/Andreas/Documents/ || echo'
```

then open `present.pdf`
