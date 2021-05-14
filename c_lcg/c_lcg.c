#include <stdio.h>

unsigned int MODULUS = 993441; // m
unsigned int MULTIPLIER = 4001; // a
unsigned int INCREMENT = 60211; // c

unsigned int gen_rand(unsigned int prev) {
    return ((prev * MULTIPLIER) + INCREMENT) % MODULUS;
}

int main() {

  unsigned int seed = 96; // aka the starting value or X0

  unsigned int out0 = gen_rand(seed);
  unsigned int out1 = gen_rand(out0);
  unsigned int out2 = gen_rand(out1);

  printf("first outputs for seed: %i \n%i\n%i\n%i\n", seed, out0, out1, out2);
}
