#include <stdio.h>
#include <assert.h>
#include "./mt_rand.c"

// 1,048,575
#define ITERATIONS 0xfffff 

int main() {
    int dummy = 0;
    for (uint32_t i = 0; i < ITERATIONS; i++) {
        php_mt_srand(i);
        
        for(uint32_t a = 0; a < 3; a++) {
           uint32_t result = php_mt_rand(); 
           if (i == 500) {
               printf("res %u = %u\n", i, result);
           }
           if (result == 1234) dummy++; 
        }
    }
    
    printf("\ndone with %i iterations (d) %i\n", ITERATIONS, dummy);
}
