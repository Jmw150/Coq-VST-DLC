struct defname {
    int int_element;
    float float_element;
};
int main ( ) {
    struct defname objname1;
    struct defname objname2;
    objname1 . int_element = objname2 . int_element ;
    objname1 . float_element = objname2 . float_element ;
    return 0 ;
}
