#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define LIMIT 10000

int main() {
    // Allocate an array of boolean values representing the sieve
    bool *is_prime = (bool *)malloc((LIMIT + 1) * sizeof(bool));
    if (is_prime == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Initialize the sieve
    for (int i = 0; i <= LIMIT; i++) {
        is_prime[i] = true;
    }

    // Mark non-prime numbers
    is_prime[0] = is_prime[1] = false; // 0 and 1 are not primes
    for (int i = 2; i * i <= LIMIT; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= LIMIT; j += i) {
                is_prime[j] = false;
            }
        }
    }

    // Count the number of primes
    int prime_count = 0;
    for (int i = 2; i <= LIMIT; i++) {
        if (is_prime[i]) {
            prime_count++;
        }
    }

    // Print the result
    printf("%d\n", prime_count);

    // Free allocated memory
    free(is_prime);

    return 0;
}
