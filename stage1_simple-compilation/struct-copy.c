// struct copy

// is a recursive problem
struct struct_name
{
    int struct_element_name;
    float flo;
};

struct bigger_struct
{
    struct struct_name s_obj;
};

/* comment */

int main ()
{
    struct struct_name object_name1;
    struct struct_name object_name2;

    // turn this
    object_name2 = object_name1; 

    // into this
    object_name2.struct_element_name = 
        object_name1.struct_element_name;

    return 0;
} 
