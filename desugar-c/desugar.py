
def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File
   
f = get_file('struct-copy.c')
print(f)

def remove_comments(string) :
    """ remove C comments
    """
    for i in range(string.len

    return string

def remove_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = string.replace(' ','')
    return string


