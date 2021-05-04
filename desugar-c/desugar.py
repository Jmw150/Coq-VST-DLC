# a mini compiler, all in one file

def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File

# some boolean functions
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
   
# scanner stuff
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

def remove_extra_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = ' '.join(string.split())
    return string

# tokenizing
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

# parsing
def id_tree(tokens:list) :
    "put markers like ID on tokens"
    # from C17 standard
    keywords = ['auto','break','case','char','const','continue','default','do','double','else','enum','extern','float','for','goto','if','inline','int','long','register','restrict','return','short','signed','sizeof','static','struct','switch','typedef','union','unsigned','void','volatile','while','_Alignas','_Alignof','_Atomic','_Bool','_Complex','_Generic','_Imaginary','_Noreturn','_Static_assert','_Thread_local']
    keywords.append('bool') # some common stuff
    keywords.append('main') 

    marked_tokens = []
    for e in tokens :
        if e in keywords :
            marked_tokens.append(e)
        elif is_identifier(e) :
            marked_tokens.append('{\'ID\':\''+e+'\'}')
        else :
            marked_tokens.append(e)

    return marked_tokens

def primitive_tree(name):
    "stuff like int, and bool, not including assigning data yet"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('ti;') : # type id ;
            # type id ;
            if (tokens[i] == name and 
                tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+2] == ';' ):
               tokens = (tokens[:i]+
                         [
                            '{\'BASETYPE\':{\'TYPE\':\''+name.upper()+'\','+
                                       tokens[i+1][1:-1]+'}}'
                         ]+
                         tokens[i+3:]) 
            i+= 1 
        return tokens
    return f

def main_tree(tokens) :
    "main from C"
    i = 0
    
    while i < len(tokens)-len('im(){r0;}') : # int main () {return 0;};
        if (tokens[i] == 'int' and
            tokens[i+1] == 'main' and
            tokens[i+2] == '(' and # NOTE: args not included for brevity
            tokens[i+3] == ')' and
            tokens[i+4] == '{') :
            print("inside main")
            j = i 
            while j < len(tokens)-len('r0;}') :
                if (tokens[j] == 'return' and 
                    tokens[j+2] == ';' and  # NOTE: not limited to be single token jumps
                    tokens[j+3] == '}') :
                    tokens = (tokens[:i] +
                             ['{\'MAIN\':'+str(tokens[i+5:j])+'}']
                             + tokens[j+4:])
                j +=1
        i+= 1
    
    return tokens


def unknown_tree(tokens) :
    "anything undefined, called last as clean up of undefined language"
    i = 0
    while i < len(tokens) :
        if (tokens[i][0] != '{' or tokens[i] == '{') : # not part of a tree
            tokens[i] = '{\'UNKNOWN\':\''+str(tokens[i])+'\'}'

        i+= 1 

    tok = []
    for e in tokens : # e is annoyingly local
        tok.append(eval(e)) 

    i = 0
    while i < len(tok) :
        if 'STRUCTDEF' in tok[i] :
            j = 0 
            while j < len(tok[i]['STRUCTDEF']['BODY']):
                tok[i]['STRUCTDEF']['BODY'][j] = eval(tok[i]['STRUCTDEF']['BODY'][j])
                j += 1
        i += 1

    return tok

def structure_init_tree(name) :
    "structs/unions as they are initialized"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('ti;') : # type id ;
            # type id ;
            if (tokens[i] == name and 
                tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+2][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+3] == ';' ):
               tokens = (tokens[:i]+
                         [
                            '{\''+name.upper()+'INIT\':'+
                                '{\'TYPE\':'+tokens[i+1][len('.ID.: '):-1]+','+
                                       tokens[i+1][1:-1]+'}}'
                         ]+
                         tokens[i+4:]) 
            i+= 1 
        return tokens
    return f

def structure_tree(name):
    "for def of unions and structs, unions and structs have the same rules"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('si{};') : # struct id { } ;
            if tokens[i] == name :
                start = i
                if tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and tokens[i+2] == '{' :
                    j = i+3
                    while tokens[j] != '}' and j < len(tokens)-len('};'):
                        j += 1
                if tokens[j] == '}' and tokens[j+1] == ';' :
                    tokens = (tokens[:start]+
                             [
                                '{\'' +str(name.upper())+ 'DEF\':{'+        # struct
                                    str(tokens[start+1][1:-1])+         # id
                                ',\'BODY\':'+str(tokens[start+3:j])+'}}' # body
                             ]
                           + tokens[j+2:])
            i+= 1
    
        return tokens 
    return f

# NOTE:need to desugar typedefs

# make the syntax trees
tree = {}
# primitives
for prime in ['char','int','float','double','_Bool'] :
    tree.update({ prime : primitive_tree(prime) })
# initialization of structs/unions
for init in ['struct','union'] :
    tree.update({ init : structure_init_tree(init) })
# declaring stuff
union_tree = structure_tree('union')
struct_tree = structure_tree('struct')


def symbol_table(tokens) :
    "start dropping those names"

    table = {}
    i = 0
    while i < len(tokens) :
        # structs
        if tokens[i][:len('{\'STRUCTDEF\':')] == '{\'STRUCTDEF\':' :
            f = eval(tokens[i])
            # eval is very surface level
            for l in f['STRUCTDEF']['BODY'] :
                l = eval(l)
            table.update({ f['STRUCTDEF']['ID'] : f })
        i += 1

    return table


# still kind of tedious conceptually
def struct_copy(tokens, s_table) :
    """ If a = b is seen, change it into a deep copy
    """

    def expand_obj(string) :
        "expands 'a' to 'a.b' if b is an element of a"
        code = []
        if string in s_table :
            for e in s_table[string]['STRUCTDEF']['BODY'] : 
                if 'BASETYPE' in e.keys() :
                    code.append(string+'.'+e['BASETYPE']['ID']) 
                elif 'STRUCTINIT' in e.keys() :
                    #code.append(string+'.'+expand_obj(e['STRUCTINIT']['TYPE'])) #NOTE: tree expansion needed
                    1
        return code

    i = 0
    while i < len(tokens)-2 :
        if (tokens[i][:len('{\'ID\':')] == '{\'ID\':' and      # found a
            tokens[i+1] == '=' and                             # found a = 
            tokens[i+2][:len('{\'ID\':')] == '{\'ID\':'):      # found a = b
            a = []
            b = []
            if tokens[i][len('{\'ID\':'):] in s_table.keys() :    # a in s_table
                a = expand_obj(tokens[i][len('{\'ID\':'):]) # expand it
            if tokens[i+2][len('{\'ID\':'):] in s_table.keys() :    # b in s_table
                b = expand_obj(tokens[i+2][len('{\'ID\':'):]) # expand

            j = 0
            while j < len(a) : # have to match up
                a[j] = a[j] + '=' + b[j]
                    
            tokens = tokens[:i] + a[:] + tokens[i+len(a):]

        i += 1

    return tokens
            
def print_types (trees) :
    " prints turns primitive types trees into strings"
    ret = ''
    i = 0
    # outside of structs, functions
    while i < len(trees) :
        if 'BASETYPE' in trees[i] :
            trees[i] = (trees[i]['BASETYPE']['TYPE'].lower() + ' ' +
                        trees[i]['BASETYPE']['ID'] + ';')
        i += 1

    return trees
    

#def main() :
f = get_file('example-program.c')

## scanning stuff
print('tokens (f)')
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print(f+'\n')

## parsing stuff
print('trees (t)')
t = raw_token(f)
t = id_tree(t)
for primitive in tree :
    t = tree[primitive](t)
#t = main_tree(t)
t = struct_tree(t)
t = unknown_tree(t)
print(str(t)+'\n')

## semantic actions
#t = struct_copy(t,s_table)
#print(t)

# code generation
print('code (p)')
p = print_types(t)
print(p)

#main()
