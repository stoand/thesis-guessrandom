# SPC-php_mt_rand
partof: REQ-purpose
###

[[.tst-php_eq_c]]

Assert that the C Mersenne Twister implementation results match those of the actual PHP functions.

```
# Install nodemon watcher
npm i -g nodemon


# Run actual PHP functions
php -e php_mt_rand/src/mt_rand.php

# Run modified C from php 8 source
(cd php_mt_rand; make watch)
```
