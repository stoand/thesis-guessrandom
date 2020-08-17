#!/bin/bash
git clone https://github.com/frangio/netlify-latex && \
cp paper/guessrandom.tex netlify-latex/main.tex && \
cd netlify-latex && bash ./build.sh main.tex

# mkdir -p build_out && \
# echo "pdf build failed" > build_out/index.html && \
# sudo apt install texlive-latex-recommended texlive-pictures texlive-latex-extra texlive-fonts-extra && \
# cd paper && \
# pdflatex guessrandom.tex && \
# cp guessrandom.pdf ../build_out && \
# cd ../build_out &&
# echo "<meta http-equiv=\"Refresh\" content=\"0; url='guessrandom.pdf'\" />" > index.html


