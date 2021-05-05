struct defname
{
    int element;
};


int main ()
{
    struct defname objname1;
    struct defname objname2;

    objname1.element = objname2.element;

    return 0;
}
