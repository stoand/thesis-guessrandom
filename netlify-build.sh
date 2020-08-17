#!/bin/bash
git clone https://github.com/frangio/netlify-latex && git checkout e62e3ca141cf3df8743b48018b66565abd4f782e && \
cp paper/guessrandom.tex netlify-latex/main.tex && \
(cd netlify-latex && bash ./build.sh main.tex) && \
mkdir -p build_out && \
cp netlify-latex/main.pdf build_out/thesis-guessrandom.pdf && \
echo "<meta http-equiv=\"Refresh\" content=\"0; url='thesis-guessrandom.pdf'\" />" > build_out/index.html


