#include <stdlib.h>
#include <stdio.h>

struct fact_entry
{                               /* Definition of each table entry */
  int n;
  char *name;
} fact_entry;

int main(int argc, const char * argv[]){

    int i, n=20;
//    char charr[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    struct fact_entry *fact_table;
    struct fact_entry tmp;

    fact_table = malloc(sizeof(fact_entry));


    if(fact_table==NULL)
    {
        fprintf(stderr, "Out of memory, exiting\n");
        exit(1);
    }


//    fact_table->n = 1;
//    fact_table->str_fact = "ABC";
//    fact_table++;
//    fact_table->n = 2;
//    fact_table->str_fact = "DEF";
//
//    printf("%d\n",(*fact_table--).n);
//    printf("%s\n",fact_table->str_fact);

    printf("%zu\n",sizeof(fact_table));

    for (i = 0; i < n; i++) {


        fact_table = realloc(fact_table, (i+1)*sizeof(fact_entry));

        if(fact_table==NULL)
        {
            fprintf(stderr, "Out of memory, exiting\n");
            exit(1);
        }

        char t[26] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        tmp.n = i+1;
        tmp.name = (t+i);//"A%d";


        (*(fact_table+i)) = tmp;

//        (*(fact_table+i)).n = i+1;

    }


    for (i = 0; i < n; i++) {

        printf(">%d %d, %s\n", i, (*(fact_table+i)).n,(*(fact_table+i)).name);

    }


    return 0;
}