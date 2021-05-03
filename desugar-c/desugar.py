
def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File
   
f = get_file('struct-copy.c')

print(f)


