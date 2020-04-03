// #SPC-php_mt_rand
#include <stdio.h>
#include <assert.h>
#include "./mt_rand.c"


// copied from "mt_rand.php" results
uint32_t php_vals[] = {1178568022, 1273124119, 1535857466};

int main() {
    php_mt_srand(0);

    printf("C mt_rand() output:\n");

	// #SPC-php_mt_rand.tst-php_eq_c
    for (uint32_t i = 0; i < 3; i++) {
        uint32_t expected = php_mt_rand();
        uint32_t actual = php_vals[i];
        
        printf("\n%u -\nexpected: %u\nactual: %u\n\n", i, expected, actual);
    	assert(expected == actual);
    }
}
