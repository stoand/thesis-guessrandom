#!/bin/bash
mkdir -p build_out && \

# Setup build script
([ -d netlify-latex ] || git clone https://github.com/frangio/netlify-latex) && \
(cd netlify-latex && git checkout 022bb08730809003db5bc5a810a9a1fee0770b6d) && \

# Build paper
cp paper/guessrandom.tex netlify-latex/main.tex && \
(cd netlify-latex && bash ./build.sh main.tex) && \
cp netlify-latex/main.pdf build_out/thesis-guessrandom.pdf && \

# Build presentation
cp present/present.tex netlify-latex/main.tex && \
(cd netlify-latex && bash ./build.sh main.tex) && \
cp netlify-latex/main.pdf build_out/thesis-guessrandom-presentation.pdf && \

echo "<meta http-equiv=\"Refresh\" content=\"0; url='thesis-guessrandom.pdf'\" />" > build_out/index.html



