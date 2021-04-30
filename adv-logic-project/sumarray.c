#include <stddef.h>

unsigned sumarray(unsigned a[], int n)
{
    int i = 0;
    unsigned s = 0;

    while(i < n)
    {
        s += a[i];
        i++;
    }

    return s;
}
// need to break the proof down on simpler code

unsigned four[4] = {1, 2, 3, 4};

int main(void)
{
    unsigned int s;
    s = sumarray(four, 4);
    return (int)s;
}


