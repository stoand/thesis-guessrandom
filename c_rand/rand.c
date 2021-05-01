#include <stdio.h>

// Taken from:
// https://stackoverflow.com/questions/4768180/rand-implementation

long holdrand;

void copy_srand(unsigned int seed) { holdrand = (long)seed; }

int copy_rand(void) {
  return (((holdrand = holdrand * 214013L + 2531011L) >> 16) & 0x7fff);
}

int main() {

  unsigned int seed = 100;

  copy_srand(100);

  int out0 = copy_rand();
  int out1 = copy_rand();
  int out2 = copy_rand();

  printf("first outputs for seed: %i \n%i\n%i\n%i\n", seed, out0, out1, out2);
}
