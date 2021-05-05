// struct assign expand 2 deep
struct defname1
{
    int int_element;
    float float_element;
};

struct defname2
{
    struct defname1 l1;
};


int main ()
{
    struct defname2 objname1;
    struct defname2 objname2;

    objname1 = objname2;

    return 0;
}
