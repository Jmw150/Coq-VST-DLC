# a mini compiler, all in one file

def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File


# boolean functions and facts
# {{{
def is_alphanum_(char) -> bool:
    return ((char >= 'a' and char <= 'z') or
            (char >= 'A' and char <= 'Z') or
            (char >= '0' and char <= '9') or
            (char == '_'))

def is_alpha_(char) -> bool:
    return ((char >= 'a' and char <= 'z') or
            (char >= 'A' and char <= 'Z') or
            (char == '_'))

def is_digit(char) -> bool :
    return (char >= '0' and char <= '9')


def is_digitdot(char) -> bool :
    return (char >= '0' and char <= '9') or char == '.'

def is_int(string) -> bool:
    for ch in string :
        if not is_digit(ch) :
            return False
    return True

def is_decimal(string) -> bool:
    if not is_digit(string[0]) :
        return False
    for ch in string :
        if not is_digitdot(ch) :
            return False
    return True

def is_identifier(string) -> bool:
    "is this string a C identifier"
    if not is_alpha_(string[0]) :
        return False
    for ch in string :
        if not is_alphanum_(ch) :
            return False
    return True


# from C17 standard
keywords = ['auto','break','case','char','const','continue','default',
        'do','double','else','enum','extern','float','for','goto','if',
        'inline','int','long','register','restrict','return','short',
        'signed','sizeof','static','struct','switch','typedef','union',
        'unsigned','void','volatile','while','_Alignas','_Alignof',
        '_Atomic','_Bool','_Complex','_Generic','_Imaginary','_Noreturn',
        '_Static_assert','_Thread_local']
keywords.append('bool') # some common stuff
keywords.append('main') 
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
def str_to_tokens(string : str) -> list :
    "the design of this is to treat characters like tokens if they are not part of the token list"

    def identifier(tokens, i) :
        "C lang identifiers"
        temp = ''
        if is_alpha_(string[i]) :
            temp += string[i]
            i += 1
            while is_alphanum_(string[i]) :
                temp += string[i]
                i += 1

            tokens.append(temp)

        return tokens, i 

    # NOTE: need all valid number types from C
    def number(tokens, i) :
        " integer, decimal  "
        temp = ''
        if is_digit(string[i]) :
            temp += string[i]
            i += 1
            while is_digitdot(string[i]) :
                temp += string[i]
                i += 1

            tokens.append(temp)

        return tokens, i 
        
    spaced_tokens : list = []

    # actual scanning part
    i = 0
    while i < len(string) :
        spaced_tokens, i = identifier(spaced_tokens, i)
        spaced_tokens, i = number(spaced_tokens, i)

        spaced_tokens.append(string[i])

        i += 1

    # remove space tokens
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
    marked_tokens = []
    for e in tokens :
        if e in keywords :
            marked_tokens.append(e)
        elif is_identifier(e) :
            marked_tokens.append('{\'ID\':\''+e+'\'}')
        else :
            marked_tokens.append(e)

    return marked_tokens

def typeinit_tree(name : str):
    "simple keywords like: int, bool"
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('tti;') : # type type id ;
               # type id ;
            if (tokens[i] == name and 
                tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+2] == ';' ) :
               tokens = (tokens[:i]+
                         [
                            '{\'TYPEINIT\':{\'TYPE\':\''+name+'\','+
                                       tokens[i+1][1:-1]+'}}'
                         ]+
                         tokens[i+3:]) 
                # type type id ;
            if (tokens[i] == name and 
                tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+2][:len('{\'ID\':')] == '{\'ID\':' and 
                tokens[i+3] == ';' ):
               tokens = (tokens[:i]+
                         [
                            '{\'TYPEINIT\':'+
                                '{\'TYPE\':'+tokens[i+1][len('{\'ID\':'):-1]+','+
                                       tokens[i+2][1:-1]+'}}'
                         ]+
                         tokens[i+4:]) 
            i+= 1 
        return tokens
    return f

def typedef_tree(name):
    """type definitions in general: struct, union, function, typedef keyword"""
    def f(tokens) :
        i = 0
        while i < len(tokens)-len('si{};') : # struct id { } ;
            # is structure
            if tokens[i] == name :
                start = i
                if tokens[i+1][:len('{\'ID\':')] == '{\'ID\':' and tokens[i+2] == '{' :
                    j = i+3
                    while tokens[j] != '}' and j < len(tokens)-len('};'):
                        j += 1
                if tokens[j] == '}' and tokens[j+1] == ';' :
                    tokens = (tokens[:start]+
                             [
                                '{\'TYPEDEF\':{'+                         # struct
                                    '\'TYPE\': \''+name+'\','+         # type
                                    str(tokens[start+1][1:-1])+','          # id
                                '\'BODY\':'+str(tokens[start+3:j])+'}}' # body
                             ]
                           + tokens[j+2:])
            i+= 1
    
        return tokens 
    return f



import typing
from typing import List 
def unknown_tree(tokens:List[str])-> List[dict] :
    "anything undefined, called last as clean up of undefined language"

    # layer rest of tokens as unknown
    i = 0
    while i < len(tokens) :
        if (tokens[i][0] != '{' or tokens[i] == '{') : # not part of a tree
            tokens[i] = '{\'UNKNOWN\':\''+str(tokens[i])+'\'}'
        if 'TYPEDEF' in tokens[i] and type(tokens[i]) != str :
            tok = tokens[i]['TYPEDEF']['BODY']
            j = 0 
            while j < len(tok):
                if (tok[j][0] != '{' or tok[j] == '{') : # not part of a tree
                    tokens[i]['TYPEDEF']['BODY'][j] = '{\'UNKNOWN\':\''+str(tok[j])+'\'}'
                j += 1
        i+= 1 
    return tokens

def intohash(tokens) :
    # turn into dictionary
    tok = []
    for e in tokens : # e is local
        tok.append(eval(e)) 

    i = 0
    while i < len(tok) :
        if 'TYPEDEF' in tok[i] :
            j = 0 
            while j < len(tok[i]['TYPEDEF']['BODY']):
                tok[i]['TYPEDEF']['BODY'][j] = eval(tok[i]['TYPEDEF']['BODY'][j])
                j += 1
        i += 1

    return tok

# make more syntax trees
tree = {}
# primitives
for prime in ['char','int','float','double','_Bool','struct','union'] :
    tree.update({ prime : typeinit_tree(prime) })
# declaring stuff
union_tree = typedef_tree('union')
struct_tree = typedef_tree('struct')

def parse(tokens) :
    "tokens to trees"

    t = str_to_tokens(tokens)
    t = id_tree(t)
    for primitive in tree :
        t = tree[primitive](t)
    t = struct_tree(t)
    t = union_tree(t)
    t = unknown_tree(t)
    t = intohash(t)

    return t

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

        # structs, and sub elements 
        if 'TYPEDEF' in trees[i] :
            table.update( { trees[i]['TYPEDEF']['ID'] : trees[i] } )
            table.update( symbol_table(trees[i]['TYPEDEF']['BODY']) )

        # primitives
        elif 'TYPEINIT' in trees[i] :
           # if not trees[i]['TYPEINIT']['TYPE'] in table :
                table.update( { trees[i]['TYPEINIT']['ID'] : trees[i] } )
        
        i += 1

    return table
# }}}

# semantic actions
# {{{

def get_parent_of(child, s_table) :

    # is own parent
    if child['ID'] in keywords : 
        return child['ID']
    
    a = s_table[ child['ID'] ]['TYPEINIT']['TYPE']
    a = s_table[a]
    return a



# NOTE: still a little complicated, more parsing would be helpful
## this should be handling things at tree level
def struct_copy(tokens, s_table) :
    """ Assuming a and b are of the same type, if a = b is seen, change it into a deep copy.
        Currently only goes one level deep

    """

    # NOTE: needs to accept a.* = b.*
    def is_a_eq_b_pattern(tokens, s_table):
        return ('ID' in tokens[i]         and 
            'UNKNOWN' in tokens[i+1]      and
            tokens[i+1]['UNKNOWN'] == '=' and
            'ID' in tokens[i+2]           and 
            tokens[i+3]['UNKNOWN'] == ';' and
            tokens[i]['ID'] in s_table    and
            'TYPEINIT' in s_table[tokens[i]['ID']])

    i = 0
    while i < len(tokens)-len('a=b;') : # bounds checking, indication that a=b could be its own tree
        # check a = b pattern is expandable
        #print(tokens[i:i+3])
        if (is_a_eq_b_pattern(tokens,s_table)): # is a struct object

            # TODO: need a way to iterate on the leaves of the tree
    
            a = get_parent_of(tokens[i],s_table)['TYPEDEF']
            #print(tokens[i], a)
            b = a 
            # make some copies
            a_body = a['BODY'][:]
            b_body = a_body[:]
            
            tokens = tokens[:i] + tokens[i+4:]

            j = 0
            while j < len(a_body) :
                # make a.x = b.x for each element
                tokens.insert(i+j*len('i.j=i.j;')+len(''), a['ID'])  # self insertion
                tokens.insert(i+j*len('i.j=i.j;')+len('.'), { 'UNKNOWN' : '.' }) 
                if 'TYPEINIT' in a_body[j] :
                 tokens.insert(i+j*len('i.j=i.j;')+len('.j'), { 'ID' : a_body[j]['TYPEINIT']['ID'] })
                if 'TYPEINIT' in a_body[j] : # TODO:make rec
                 tokens.insert(i+j*len('i.j=i.j;')+len('.j'), { 'ID' : a_body[j]['TYPEINIT']['ID'] })

                tokens.insert(i+j*len('i.j=i.j;')+len('.j='), { 'UNKNOWN' : '=' }) 

                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i'), { 'ID' : b['ID'] })
                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i.'), { 'UNKNOWN' : '.' }) 
                if 'TYPEINIT' in b_body[j] :
                 tokens.insert( i+j*len('i.j=i.j;')+len('.j=i.j'), { 'ID' : b_body[j]['TYPEINIT']['ID'] })
                if 'TYPEINIT' in b_body[j] : # TODO:make rec
                 tokens.insert( i+j*len('i.j=i.j;')+len('.j=i.j'), { 'ID' : b_body[j]['TYPEINIT']['ID'] })
                
                tokens.insert(i+j*len('i.j=i.j;')+len('.j=i.j;'), { 'UNKNOWN' : ';' }) 
                j += 1
        i += 1

    return tokens
# }}}

# code generation
# {{{
def codegen_types (trees,s_table) :
    " prints turns types trees into strings"
    # outside of structs, functions

    primitive_list = ['int','char','float','double','bool'] # TODO: check standard
    i = 0
    while i < len(trees) :
        # base case
        if 'TYPEINIT' in trees[i] :
            Typeinit = trees[i]['TYPEINIT']

            # primitive
            if Typeinit['TYPE'] in primitive_list :
                trees[i] = (Typeinit['TYPE'] + ' ' + Typeinit['ID'] + ';')
            else :
            # user defined
                trees[i] = ('struct ' #get_parent_of(Typeinit, s_table)['TYPEDEF']['TYPE']
                         + Typeinit['TYPE'] + ' ' + Typeinit['ID'] + ';')

        # recursive case
        if 'TYPEDEF' in trees[i] :
            trees[i]['TYPEDEF']['BODY'] = codegen_types(trees[i]['TYPEDEF']['BODY'],s_table)
        i += 1

    return trees
    
def codegen_list(strings: List[str])->str :
    s = ''
    for e in strings :
        s += e + ' ' 
    return s

def codegen_struct(trees : List[dict]) :
    i = 0
    while i < len(trees) :
        if 'TYPEDEF' in trees[i] :
            trees[i] = (
                trees[i]['TYPEDEF']['TYPE'] +
                trees[i]['TYPEDEF']['ID'] + 
                ' {' +
                    codegen_list(trees[i]['TYPEDEF']['BODY']) +
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

def code_generation(trees,s_table) :
    c = codegen_types(trees,s_table)
    c = codegen_struct(c)
    c = codegen_leafs(c)
    c = codegen_list(c)
    return c
    
# }}}


#def main() :
f = get_file('example-program.c')

## scanning stuff
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print('tokens (f)\n'+ f+'\n')

## parsing stuff
t = parse(f)
#print('trees (t)\n')
#for b in t : print(b)

# symbol table
st = symbol_table(t)
print('symbol table (st)')
#for s in st : print(s, st[s])

## semantic actions
#print('semantic actions (t)')
t = struct_copy(t,st)
#print(t)

# code generation
print('code (c)')
c = code_generation(t,st)
print(c)

#main()
