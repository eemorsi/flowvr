/**
 * gcc -O2 putter.c -o cputter -I$HOME/pdi/build/include -L$HOME/pdi/build/lib -lpdi -lparaconf -lyaml 
 **/

#include <stdio.h>
#include <unistd.h>

#include <pdi.h>

int main()
{
    PC_tree_t node = PC_parse_path("put.yml");
    PDI_init(PC_get(node, ".pdi"));

    int wait = 1;
    int scalar = 0;
    int size;
    PDI_expose("wait", &wait, PDI_IN);
    while (scalar < 10)
    {
        size = scalar < 5 ? (scalar + 1) * 1000 : 5000;
        PDI_expose("scalar", &size, PDI_OUT);
        // printf("C scalar: %d\n", scalar);
        if (scalar == 10)
        {
            wait = 0;

            break;
        }
        else
        {
            scalar++;
            sleep(2);
            PDI_expose("wait", &wait, PDI_IN);
        }
    }
    PDI_expose("wait", &wait, PDI_IN);

    PDI_finalize();
    return 0;
}
