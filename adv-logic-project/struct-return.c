// struct return


struct foo
{
    int bar;
};

struct foo wrap_int (int i)
{
    struct foo f;
    f.bar = i;
    return f;
}

int main ()
{
    return 0;
}
