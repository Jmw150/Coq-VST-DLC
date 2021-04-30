# change a C duff machine to a simple loop
#TODO: make functions lazy for streams

import os.path

def file_to_str(filename) -> str :
    
    if not os.path.isfile(filename):
        print('File does not exist.')
    else:
        # Open the file as f.
        # The function readlines() reads the file.
        with open(filename) as f:
            content = f.read()

    return content

def squish_duff_machine (code:str) -> str :
    "return the c program without a duff machine in it"
    
    def duff_tokens(code:str) :
        "tokens that matter in a duff machine"

        # cases inside of a scope seem to be a defining feature
        """
            flag: switch*name*{*case*}*

            error: unsupported feature: 'case' statement not in 'switch' statement
            
        """
        tokens = [
            'switch',
            'do',
            'case',
            'while'
        ]
        for symbol in code :
            
        

print(file_to_str("duff.c"))
