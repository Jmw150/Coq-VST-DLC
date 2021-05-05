struct defname1
{
    int int_element;
    float float_element;
};

struct defname2
{
    struct defname1 l1;
    int leaf;
};

typedef struct defname2 shorttype;

int main ()
{
    struct defname2 objname1;
    struct defname2 objname2;

    objname1.l1.int_element = objname2.l1.int_element;
    objname1.l1.float_element = objname2.l1.float_element;
    objname1.leaf = objname2.leaf;

    return 0;
}
