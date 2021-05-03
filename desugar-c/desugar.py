
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


def token(string) :
    "the design of this is to treat characters like tokens if they are not part of the token list"

    def pull_token(tokens:list, i:int, token:str) :
        if string[i:i+len(token)] == token :
            tokens.append(token)
            i += len(token)

        return tokens, i

    def is_alphanum_(string,i):
        return ((string[i] >= 'a' and string[i] <= 'z') or
                (string[i] >= 'A' and string[i] <= 'Z') or
                (string[i] >= '0' and string[i] <= '9') or
                (string[i] == '_'))

    
    def is_alpha_(string,i):
        return ((string[i] >= 'a' and string[i] <= 'z') or
                (string[i] >= 'A' and string[i] <= 'Z') or
                (string[i] == '_'))

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
        #tokens, i = pull_token(tokens, i, 'struct')
        tokens, i = identifier(spaced_tokens, i)

        spaced_tokens.append(string[i])

        i += 1

    # remove spaces
    tokens = []
    for e in spaced_tokens :
        if e != ' ' :
            tokens.append(e)

    # label idendifiers
    for e in tokens :

    return tokens

def remove_newlines(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    return string

def remove_extra_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = ' '.join(string.split())
    return string

def remove_whitespace(string) :
    string = string.replace('\r','')
    string = string.replace('\n','')
    string = string.replace(' ','')
    return string

#def main() :
f = get_file('struct-copy.c')
f = remove_single_comments(f)
f = remove_multi_comments(f)
f = remove_extra_whitespace(f)
print(f)
t = token(f)
print(t)

#main()
