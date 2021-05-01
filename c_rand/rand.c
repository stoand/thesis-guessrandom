#include <stdio.h>

// Taken from:
// https://stackoverflow.com/questions/4768180/rand-implementation

long holdrand;

void copy_srand(unsigned int seed) { holdrand = (long)seed; }

int copy_rand(void) {
  return (((holdrand = holdrand * 214013L + 2531011L) >> 16) & 0x7fff);
}

int main() { printf("hello\n"); }
