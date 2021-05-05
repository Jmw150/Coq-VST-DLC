// This program is used to test if basic grammar is working
/* comment */

// simple structures
int some_int;
float some_float;

// structures can be called like this
struct struct_name
{
    int struct_element_name;
    float flo;
};

union union_name {
    int u_int;
    floar u_int;
};

// scope of structures
struct bigger_struct
{
    struct struct_name s_obj;
};

struct even_bigger_struct
{
    struct bigger_struct bs_obj;
    int struct_leaf;
};

typedef even_bigger_struct ebs;

int main ()
{
    struct struct_name object_name1;
    struct struct_name object_name2;

    // turn this
    object_name2 = object_name1; 

    // into this
    //object_name2.struct_element_name = object_name1.struct_element_name;

    return 0;
} 
