# a mini compiler, all in one file

def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File


# some boolean functions
# {{{
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
# }}}
   
# clean up code
# {{{
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
# }}}

# tokenizing
# {{{
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
# }}}

# parsing
# {{{
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
                                       tokens[i+2][1:-1]+'}}'
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

def function_tree(tokens) :
    "functions from C"
    i = 0
    
    while i < len(tokens)-len('im(){r0;}') : # int main () {return 0;};
        if (tokens[i] == 'int' and
            tokens[i+1][len('ID:')] == 'ID:' and
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
                             ['{\'FUNCTION\':'+str(tokens[i+5:j])+'}']
                             + tokens[j+4:])
                j +=1
        i+= 1
    
    return tokens

# operator tree maker
def operator_tree(operator):
    def f(tokens):
        return tokens
    return f

# assignment tree
def assignment_tree(tokens):
    " a = b "
    
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

# }}}

# symbol table
# {{{
# NOTE: scope not included
def symbol_table(trees) :
    "a table of names in the program"
    #start dropping those names

    table = {}
    i = 0
    while i < len(trees) :

        # structs
        if 'STRUCTDEF' in trees[i] :
            table.update( { trees[i]['STRUCTDEF']['ID'] : trees[i] } )

        # struct objects, only if previously defined (rule from C)
        if 'STRUCTINIT' in trees[i] :
            if trees[i]['STRUCTINIT']['TYPE'] in table :
                table.update( { trees[i]['STRUCTINIT']['ID'] : trees[i] } )

        # global primitive types
        if 'BASETYPE' in trees[i] :
            table.update( { trees[i]['BASETYPE']['ID'] : trees[i] } )
        
        i += 1

    return table
# }}}

# semantic actions
# {{{
# NOTE: still a little complicated, more parsing would be helpful
## this should be handling things at tree level
def struct_copy(tokens, s_table) :
    """ Assuming a and b are of the same type, if a = b is seen, change it into a deep copy.
        Currently only goes one level deep

    """

    def is_a_eq_b_pattern(tokens, s_table):
        return ('ID' in tokens[i]             and 
            'UNKNOWN' in tokens[i+1]      and
            'ID' in tokens[i+2]           and 
            tokens[i+1]['UNKNOWN'] == '=' and
            tokens[i+3]['UNKNOWN'] == ';' and
            tokens[i]['ID'] in s_table    and
            'STRUCTINIT' in s_table[tokens[i]['ID']])

    i = 0
    while i < len(tokens)-len('a=b;') : # bounds checking, indication that a=b could be its own tree

        # check a = b pattern is expandable
        if (is_a_eq_b_pattern(tokens,s_table)): # is a struct object

            # TODO: need a way to iterate on the leaves of the tree
            a = s_table[
                    s_table[
                        tokens[i]['ID'] # name of object
                           ]
                        ['STRUCTINIT']['TYPE'] # name of definition
                       ]['STRUCTDEF'] # parts of 'a'
            b = a 
            # make some copies
            a_body = a['BODY'][:]
            b_body = b['BODY'][:]

            tokens = tokens[:i] + tokens[i+4:]

            j = 0
            while j < len(a_body) :
                # make a.x = b.x for each element
                tokens.insert(i+j*len('i.j=i.j;')+len(''), a['ID'])  # self insertion
                tokens.insert(i+j*len('i.j=i.j;')+len('.'), { 'UNKNOWN' : '.' }) 
                if 'BASETYPE' in a_body[j] :
                 tokens.insert(i+j*len('i.j=i.j;')+len('.j'), { 'ID' : a_body[j]['BASETYPE']['ID'] })
                if 'STRUCTINIT' in a_body[j] : # TODO:make rec
                 tokens.insert(i+j*len('i.j=i.j;')+len('.j'), { 'ID' : a_body[j]['STRUCTINIT']['ID'] })

                tokens.insert(i+j*len('i.j=i.j;')+len('.j='), { 'UNKNOWN' : '=' }) 

                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i'), { 'ID' : b['ID'] })
                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i.'), { 'UNKNOWN' : '.' }) 
                if 'BASETYPE' in b_body[j] :
                 tokens.insert( i+j*len('i.j=i.j;')+len('.j=i.j'), { 'ID' : b_body[j]['BASETYPE']['ID'] })
                if 'STRUCTINIT' in b_body[j] : # TODO:make rec
                 tokens.insert( i+j*len('i.j=i.j;')+len('.j=i.j'), { 'ID' : b_body[j]['STRUCTINIT']['ID'] })
                
                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i.j;'), { 'UNKNOWN' : ';' }) 
                j += 1
        i += 1

    return tokens
# }}}

# code generation
# {{{
# NOTE:need to desugar typedefs
def codegen_types (trees) :
    " prints turns primitive types trees into strings"
    # outside of structs, functions
    i = 0
    while i < len(trees) :
        if 'BASETYPE' in trees[i] :
            trees[i] = (trees[i]['BASETYPE']['TYPE'].lower() + ' ' +
                        trees[i]['BASETYPE']['ID'] + ';')
        i += 1

    # inside structs
    i = 0
    while i < len(trees) :
        if 'STRUCTDEF' in trees[i] :
            j = 0
            while j < len(trees[i]['STRUCTDEF']['BODY']) :
                if 'BASETYPE' in trees[i]['STRUCTDEF']['BODY'][j] :
                    trees[i]['STRUCTDEF']['BODY'][j] = (
                        trees[i]['STRUCTDEF']['BODY'][j]['BASETYPE']['TYPE'].lower() + ' ' +
                        trees[i]['STRUCTDEF']['BODY'][j]['BASETYPE']['ID'] + ';')
                j += 1 
        i += 1 

    return trees
    
def codegen_structinit(trees) :
    " prints turns struct initialization trees into strings"
    # outside of structs, functions
    i = 0
    while i < len(trees) :
        if 'STRUCTINIT' in trees[i] :
            trees[i] = (
                'struct ' +
                trees[i]['STRUCTINIT']['TYPE'].lower() + ' ' +
                trees[i]['STRUCTINIT']['ID'] + ';')
        i += 1

    # inside structs
    i = 0
    while i < len(trees) :
        if 'STRUCTDEF' in trees[i] :
            j = 0
            while j < len(trees[i]['STRUCTDEF']['BODY']) :
                if 'STRUCTINIT' in trees[i]['STRUCTDEF']['BODY'][j] :
                    trees[i]['STRUCTDEF']['BODY'][j] = (
                        'struct ' +
                        trees[i]['STRUCTDEF']['BODY'][j]['STRUCTINIT']['TYPE'].lower() + ' ' +
                        trees[i]['STRUCTDEF']['BODY'][j]['STRUCTINIT']['ID'] + ';')
                j += 1 
        i += 1

    return trees

def codegen_list(strings) :
    s = ''
    for e in strings :
        s += e + ' ' 
    return s

def codegen_struct(trees) :
    i = 0
    while i < len(trees) :
        if 'STRUCTDEF' in trees[i] :
            trees[i] = (
                'struct ' +
                trees[i]['STRUCTDEF']['ID'].lower() + ' {' +
                codegen_list(trees[i]['STRUCTDEF']['BODY']) +
                '};') 
        i += 1

    return trees
    
def codegen_leafs(trees) :
    'single structures like ID and unknown '
    i = 0
    while i < len(trees) :
        if 'ID' in trees[i] :
            trees[i] = trees[i]['ID']
        i += 1
        
    i = 0
    while i < len(trees) :
        if 'UNKNOWN' in trees[i] :
            trees[i] = trees[i]['UNKNOWN']
        i += 1

    return trees
# }}}


#def main() :
f = get_file('example-program.c')

## scanning stuff
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print('tokens (f)\n'+ f+'\n')

## parsing stuff
t = raw_token(f)
t = id_tree(t)
for primitive in tree :
    t = tree[primitive](t)
t = struct_tree(t)
t = unknown_tree(t)
print('trees (t)\n'+ str(t)+'\n')

# symbol table
st = symbol_table(t)
print('symbol table (st)')
for s in st :
    print(s, st[s])

## semantic actions
print('semantic actions (t)')
t = struct_copy(t,st)
#print(t)

# code generation
print('code (c)')
c = codegen_types(t)
c = codegen_structinit(c)
c = codegen_struct(c)
c = codegen_leafs(c)
c = codegen_list(c)
print(c)

#main()
