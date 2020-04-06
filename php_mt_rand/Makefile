all:
	clang -fsanitize=address src/test_mt_rand.c -o test && ./test
watch:
	nodemon -e c -x 'make || echo'
run-bench:
	clang -O3 src/bench_mt_rand.c -o bench && echo && time ./bench
