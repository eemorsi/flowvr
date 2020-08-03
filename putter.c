/**
 * 
 * gcc -O2 putter.c -o cputter -I$HOME/pdi/build/include -L$HOME/pdi/build/lib -lpdi -lparaconf -lyaml 
 **/


#include <stdio.h>
#include <unistd.h>

#include <pdi.h>

int main() {
    PC_tree_t node = PC_parse_path("put.yml");
    PDI_init(PC_get(node, ".pdi"));

    int wait;
    int scalar = 0;
    PDI_expose("wait", &wait, PDI_IN);
    while (wait) {
        PDI_expose("scalar", &scalar, PDI_OUT);
        printf("C scalar: %d\n", scalar);
        
        PDI_expose("wait", &wait , PDI_IN);
        scalar++;
        sleep(2);
    }

    PDI_finalize();
    return 0;
}
