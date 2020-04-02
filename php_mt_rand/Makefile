all:
	clang -fsanitize=address src/main.c -o run && ./run
watch:
	nodemon -e c -x 'make || echo'
