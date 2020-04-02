#include <stdio.h>
#include "./mt_rand.c"

int main() {
    php_mt_srand(0);
    printf("C mt_rand() output:\n");
    printf("%u\n", php_mt_rand());
    printf("%u\n", php_mt_rand());
    printf("%u\n", php_mt_rand());
}
