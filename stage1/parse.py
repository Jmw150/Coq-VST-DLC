# a mini compiler, all in one file

def get_file(filename) :
    File = ''
    with open(filename) as f:
        for l in f.readlines() :
            File += l

    return File


# some boolean functions
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

    marked_tokens = []
    for e in tokens :
        if e in keywords :
            marked_tokens.append(e)
        elif is_identifier(e) :
            marked_tokens.append('{\'ID\':\''+e+'\'}')
        else :
            marked_tokens.append(e)

    return marked_tokens

def type_tree(name : str):
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
                            '{\'TYPEINIT\':{\'TYPE\':\''+name+'\','+
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

import typing
from typing import List 
def unknown_tree(tokens:List[str])-> List[dict] :
    "anything undefined, called last as clean up of undefined language"

    # layer rest of tokens as unknown
    i = 0
    while i < len(tokens) :
        if (tokens[i][0] != '{' or tokens[i] == '{') : # not part of a tree
            tokens[i] = '{\'UNKNOWN\':\''+str(tokens[i])+'\'}'
        if 'STRUCTDEF' in tokens[i] and type(tokens[i]) != str :
            tok = tokens[i]['STRUCTDEF']['BODY']
            j = 0 
            while j < len(tok):
                if (tok[j][0] != '{' or tok[j] == '{') : # not part of a tree
                    tokens[i]['STRUCTDEF']['BODY'][j] = '{\'UNKNOWN\':\''+str(tok[j])+'\'}'
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
        if 'STRUCTDEF' in tok[i] :
            j = 0 
            while j < len(tok[i]['STRUCTDEF']['BODY']):
                tok[i]['STRUCTDEF']['BODY'][j] = eval(tok[i]['STRUCTDEF']['BODY'][j])
                j += 1
        i += 1

    return tok

# make more syntax trees
tree = {}
# primitives
for prime in ['char','int','float','double','_Bool','struct','union'] :
    tree.update({ prime : type_tree(prime) })
# declaring stuff
union_tree = structure_tree('union')
struct_tree = structure_tree('struct')

def parse(tokens) :
    "tokens to trees"

    t = str_to_tokens(tokens)
    t = id_tree(t)
    for primitive in tree :
        t = tree[primitive](t)
    t = struct_tree(t)
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

        # structs
        if 'STRUCTDEF' in trees[i] :
            table.update( { trees[i]['STRUCTDEF']['ID'] : trees[i] } )

        # struct objects, only if previously defined (rule from C)
# NOTE need to check for primitives now
        if 'TYPEINIT' in trees[i] :
            if trees[i]['TYPEINIT']['TYPE'] in table :
                table.update( { trees[i]['TYPEINIT']['ID'] : trees[i] } )
        
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
        if (is_a_eq_b_pattern(tokens,s_table)): # is a struct object

            # TODO: need a way to iterate on the leaves of the tree
            a = s_table[
                    s_table[
                        tokens[i]['ID'] # name of object
                           ]
                        ['TYPEINIT']['TYPE'] # name of definition
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
def codegen_types (trees) :
    " prints turns types trees into strings"
    # outside of structs, functions

    primitive_list = ['int','char','float','double','bool'] # TODO: check standard
    i = 0
    while i < len(trees) :
        if 'TYPEINIT' in trees[i] :
            Typeinit = trees[i]['TYPEINIT']
            if Typeinit['TYPE'] in primitive_list :
                trees[i] = (Typeinit['TYPE'] + ' ' + Typeinit['ID'] + ';')
            else :
                trees[i] = ('struct ' + Typeinit['TYPE'] + ' ' + Typeinit['ID'] + ';')
                
        i += 1

    # inside structs
    i = 0
    while i < len(trees) :
        if 'STRUCTDEF' in trees[i] :
            j = 0
            while j < len(trees[i]['STRUCTDEF']['BODY']) :
                if 'TYPEINIT' in trees[i]['STRUCTDEF']['BODY'][j] :
                    Typeinit = trees[i]['STRUCTDEF']['BODY'][j]['TYPEINIT']
                    if Typeinit['TYPE'] in primitive_list :
                        trees[i] = (Typeinit['TYPE'] + ' ' +
                                    Typeinit['ID'] + ';')
                    else :
                        trees[i] = ('struct ' + Typeinit['TYPE'] + ' ' +
                                    Typeinit['ID'] + ';')
                j += 1 
        i += 1 

    return trees
    
def codegen_list(strings: List[str])->str :
    s = ''
    for e in strings :
        print(e)
        s += e + ' ' 
    return s

def codegen_struct(trees : List[dict]) :
    i = 0
    while i < len(trees) :
        if 'STRUCTDEF' in trees[i] :
            trees[i] = (
                'struct ' +
                trees[i]['STRUCTDEF']['ID'] + ' {' +
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
#print('tokens (f)\n'+ f+'\n')

## parsing stuff
t = parse(f)
print('trees (t)\n'+ str(t)+'\n')

# symbol table
#st = symbol_table(t)
#print('symbol table (st)')
#for s in st : print(s, st[s])

## semantic actions
#print('semantic actions (t)')
#t = struct_copy(t,st)
#print(t)

# code generation
#print('code (c)')
#c = codegen_types(t)
#c = codegen_struct(c)
#c = codegen_leafs(c)
#c = codegen_list(c)
#print(c)

#main()
