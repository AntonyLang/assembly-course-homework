#include <stdint.h>
#include <stdio.h>

typedef struct {
    uint16_t word[5];
} Big;

static Big cache[101];
static unsigned char ready[101];

void fib(unsigned n, Big *value)
{
    Big a, b;
    uint32_t carry = 0;
    unsigned i;

    if (ready[n]) {
        *value = cache[n];
        return;
    }
    if (n < 2) {
        cache[n].word[0] = (uint16_t)n;
    } else {
        fib(n - 1, &a);
        fib(n - 2, &b);
        for (i = 0; i < 5; ++i) {
            carry += (uint32_t)a.word[i] + b.word[i];
            cache[n].word[i] = (uint16_t)carry;
            carry >>= 16;
        }
    }
    ready[n] = 1;
    *value = cache[n];
}

void print_big(Big value)
{
    char digits[25];
    unsigned count = 0;
    uint32_t remainder;
    unsigned nonzero;
    int i;

    do {
        remainder = 0;
        nonzero = 0;
        for (i = 4; i >= 0; --i) {
            uint32_t part = (remainder << 16) | value.word[i];
            value.word[i] = (uint16_t)(part / 10);
            remainder = part % 10;
            nonzero |= value.word[i];
        }
        digits[count++] = (char)('0' + remainder);
    } while (nonzero);
    while (count) {
        putchar(digits[--count]);
    }
}

int main(void)
{
    unsigned n;
    Big value;

    printf("Input n (1..100): ");
    scanf("%u", &n);
    fib(n, &value);
    printf("F(n): ");
    print_big(value);
    putchar('\n');
    return 0;
}
