// struct assign expand with typedef
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
    shorttype objname1;
    shorttype objname2;

    objname1 = objname2;

    return 0;
}
