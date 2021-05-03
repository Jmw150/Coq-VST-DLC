
def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File
   

def remove_single_comments(string) :
    """ remove C comments
    """
    i = 0
    while i < len(string) :
        if string[i:i+2] == '//' : # skipping single line 
            j = i
            while string[j] != '\n' and j < len(string):
                j += 1
            string = string[0:i] + string[j:]
        i += 1
            
    return string

def remove_multi_comments(string) :
    i = 0
    while i < len(string) :
        if string[i:i+2] == '/*' : # skipping single line 
            j = i
            while string[j:j+2] != '*/' and j < len(string):
                j += 1
            string = string[0:i] + string[j+2:]
        i += 1
    return string

def is_alphanum_(string,i):
    return ((string[i] >= 'a' and string[i] <= 'z') or
            (string[i] >= 'A' and string[i] <= 'Z') or
            (string[i] >= '0' and string[i] <= '9') or
            (string[i] == '_'))

def is_alpha_(string,i):
    return ((string[i] >= 'a' and string[i] <= 'z') or
            (string[i] >= 'A' and string[i] <= 'Z') or
            (string[i] == '_'))

def is_identifier(string):
    "is this string a C identifier"
    if not is_alpha_(string, 0) :
        return False
    for ch in string :
        if not (is_alpha_(ch, 0) or is_alphanum_(ch, 0)) :
            return False
    return True

def raw_token(string) :
    "the design of this is to treat characters like tokens if they are not part of the token list"

    def identifier(tokens, i) :
        temp = ''
        if is_alpha_(string, i) :
            temp += string[i]
            i += 1
            while is_alphanum_(string, i) :
                temp += string[i]
                i += 1

            tokens.append(temp)

        return tokens, i 
        
    spaced_tokens = []
    i = 0
    while i < len(string) :
        spaced_tokens, i = identifier(spaced_tokens, i)

        spaced_tokens.append(string[i])

        i += 1

    # remove spaces
    tokens = []
    for e in spaced_tokens :
        if e != ' ' :
            tokens.append(e) 

    return tokens

def ast_token(tokens:list) :
    "put markers like ID on tokens"
    # from C17 standard
    keywords = [
        'auto','break','case','char','const','continue','default','do','double','else','enum','extern','float','for','goto','if','inline','int','long','register','restrict','return','short','signed','sizeof','static','struct','switch','typedef','union','unsigned','void','volatile','while','_Alignas','_Alignof','_Atomic','_Bool','_Complex','_Generic','_Imaginary','_Noreturn','_Static_assert','_Thread_local']
    keywords.append('bool') # some common stuff
    keywords.append('main') 


    marked_tokens = []
    for e in tokens :
        if e in keywords :
            marked_tokens.append(e)
        elif is_identifier(e) :
            marked_tokens.append('ID:'+e)
        else :
            marked_tokens.append(e)

    return marked_tokens

# NOTE:need to desugar typedefs
def primitive_tree(name):
    "stuff like int, and bool, not including assigning data yet"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('ti;') : # type id ;
            # type id ;
            if tokens[i] == name :
                if tokens[i+1][:len('ID:')] == 'ID:' :
                    if tokens[i+2] == ';' :
                        tokens = (tokens[:i]+
                                 [name.upper()+':'+tokens[i+1][len('ID:'):]]+
                                  tokens[i+3:]) 
            i+= 1 
        return tokens
    return f
        

def structure_tree(name):
    "for def of unions and structs, unions and structs have the same rules"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('si{};') : # length of empty struct
            if tokens[i] == name :
                start = i
                if tokens[i+1][:len('ID:')] == 'ID:' and tokens[i+2] == '{' :
                    j = i+3
                    while tokens[j] != '}' and j < len(tokens)-len('};'):
                        j += 1
                if tokens[j] == '}' and tokens[j+1] == ';' :
                    tokens = (tokens[:start]
                           + [name.upper()+':'+'\''+str(tokens[start+1][3:])+'\':'+str(tokens[start+3:j])]
                           + tokens[j+2:])
            i+= 1
    
        return tokens 
    return f

# make the syntax trees
tree = {}
for prime in ['char','int','float','double','_Bool'] :
    tree.update({ prime : primitive_tree(prime) })
union_tree = structure_tree('union')
struct_tree = structure_tree('struct')


def struct_table(tokens) :
    "pull out and store struct syntax trees"

    table = {}
    i = 0
    while i < len(tokens) :
        # hand code grammar
        if tokens[i][:len('STRUCT:')] == 'STRUCT:' :
            table.update(eval(
                    str('{'+tokens[i][len('STRUCT:'):]+'}')
                ))

        i += 1

    return table

def remove_extra_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = ' '.join(string.split())
    return string

def struct_copy(tokens, s_table) :
    """ If a = b is seen, change it into a deep copy
    """

    def expand_obj(string) :
        return string

    i = 0
    while i < len(tokens)-2 :
        if (tokens[i][:len('ID:')] == 'ID:' and
            tokens[i+1] == '=' and
            tokens[i+2][:len('ID:')] == 'ID:'):
            if tokens[i][len('ID:'):] in s_table.keys() :
                tokens[i] = expand_obj(tokens[i][len('ID:'):])
            if tokens[i+2][len('ID:'):] in s_table.keys() :
                tokens[i+2] = expand_obj(tokens[i+2][len('ID:'):])


#def main() :
f = get_file('struct-copy.c')
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print(f)
t = raw_token(f)
t = ast_token(t)

for primitive in tree :
    t = tree[primitive](t)
t = struct_tree(t)

print(t)
s_table = struct_table(t)
print(s_table)

#main()
