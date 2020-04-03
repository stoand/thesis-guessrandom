all:
	clang -fsanitize=address src/test_mt_rand.c -o test && ./test
watch:
	nodemon -e c -x 'make || echo'
