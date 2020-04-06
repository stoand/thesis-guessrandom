#include <stdio.h>
#include <assert.h>
#include "./mt_rand.c"

// 1,048,575
#define ITERATIONS 0xfffff 

int main() {
    int dummy = 0;
    for (uint32_t i = 0; i < ITERATIONS; i++) {
        php_mt_srand(i);
        php_mt_reload();
        
        for(uint32_t a = 0; a < 3; a++) {
           if (php_mt_rand() == 1234) dummy++; 
        }
    }
    
    printf("\ndone with %i iterations (d) %i\n", ITERATIONS, dummy);
}
