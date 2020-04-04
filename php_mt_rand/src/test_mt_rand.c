// #SPC-php_mt_rand
#include <stdio.h>
#include <assert.h>
#include "./mt_rand.c"


// copied from "mt_rand.php" results
uint32_t php_vals[] = {1489665453,160506331,132536224};

int main() {
    php_mt_srand(500);

	// #SPC-php_mt_rand.tst-php_eq_c
    for (uint32_t i = 0; i < 3; i++) {
        uint32_t expected = php_mt_rand();
        uint32_t actual = php_vals[i];

        if (expected != actual) {
            printf("\n%u -\nexpected: %u\nactual: %u\n\n", i, expected, actual);
        }
    	assert(expected == actual);
    }
}
