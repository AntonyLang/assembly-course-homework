#include <stdio.h>

int main(void)
{
    int letter = 'a';
    int row;
    int column;

    for (row = 0; row < 2; ++row) {
        for (column = 0; column < 13; ++column) {
            putchar(letter);
            ++letter;
            if (column < 12) {
                putchar(' ');
            }
        }
        putchar('\n');
    }

    return 0;
}
