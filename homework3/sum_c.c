/* Homework 3: valid input is one decimal integer n in 1..100. */
#include <stdio.h>

int main(void)
{
    int n;
    int i;
    unsigned int total = 0;

    printf("Input n (1..100): ");
    scanf("%d", &n);
    for (i = 1; i <= n; ++i) {
        total += i;
    }
    printf("Sum: %u\n", total);
    return 0;
}
