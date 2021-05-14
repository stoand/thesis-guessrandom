#include <stdio.h>

int MODULUS = 993441; // m
int MULTIPLIER = 4001; // a
int INCREMENT = 60211; // c

int gen_rand(int prev) {
    // TODO - add the modulus back
    // return ((prev * MULTIPLIER) + INCREMENT) % MODULUS;
    return ((prev * MULTIPLIER) + INCREMENT);
}

int main() {

  int seed = 96; // aka the starting value or X0

  int out0 = gen_rand(seed);
  int out1 = gen_rand(out0);
  int out2 = gen_rand(out1);

  printf("first outputs for seed: %i \n%i\n%i\n%i\n", seed, out0, out1, out2);
}
