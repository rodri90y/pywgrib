#include <stdlib.h>
#include <stdio.h>


char *increment_string(char *str, int n)
{
  for (int i = 0; str[i]; i++)
    str[i] = str[i] + n;
  return (str);
}
