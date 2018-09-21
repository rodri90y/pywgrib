#include <stdlib.h>
#include <stdio.h>

typedef struct point {
    int x;
    float *y;
} POINT;

POINT *get_point()
{
    POINT *p;
    float data[4] =  {1,2,3,4};

    POINT initial = {1,data};

    p = malloc(sizeof(POINT));
    *p = initial;

    return p;
}

void free_point(POINT *p)
{
    free(p);
}