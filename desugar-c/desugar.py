
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
    keywords.append('bool') # common
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
def struct_tree(tokens) :
    "make struct trees in the token list"
    temp = []
    i = 0
    while i < len(tokens)-len('si{};') : # length of empty struct
        if tokens[i] == 'struct' :
            start = i
            if tokens[i+1][:len('ID:')] == 'ID:' and tokens[i+2] == '{' :
                j = i+3
                while tokens[j] != '}' and j < len(tokens)-len('};'):
                    j += 1
            if tokens[j] == '}' and tokens[j+1] == ';' :
                tokens = (tokens[:start]
                       + ['STRUCT:'+str(tokens[start+1][3:])+':'+str(tokens[start+3:j])]
                       + tokens[j:])
        i+= 1

    return tokens
            
            

def struct_table(table) :
    "pull out and store struct syntax trees"

    i = 0
    while i < len(table) :
        # hand code grammar
        if table[i] == 'struct' :
            1

def remove_extra_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = ' '.join(string.split())
    return string


#def main() :
f = get_file('struct-copy.c')
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print(f)
t = raw_token(f)
#print(t)
t = ast_token(t)
#print(t)
t = struct_tree(t)
print(t)

#main()
