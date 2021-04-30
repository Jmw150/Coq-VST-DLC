// struct copy
//
// is a recursive problem
// 
struct struct_name
{
    int struct_element_name;
};



int main ()
{
    struct struct_name object_name1;
    struct struct_name object_name2;

    object_name2 = object_name1; 

    /* // instead have
    object_name2.struct_element_name = object_name1.struct_element_name; 
    */

    return 0;
} 
