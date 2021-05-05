// struct parameters
//
// is a recursive problem
struct lol
{
    int cat;
};

struct lolad
{
    struct lol ad2;
};

int main ()
{
    
    struct lol some_random = {1}; 

    //struct lol some_random;
    //some_random.cat = 1;


    struct lolad a = {{1}};

    return 0;
}
