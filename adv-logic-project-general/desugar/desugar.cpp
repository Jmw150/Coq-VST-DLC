// A simple program transformer

#include <cctype>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <queue>
#include <memory>
#include <string>
#include <utility>
#include <vector>
#include <functional>
#include <iostream>

// no interest in reinventing standard wheels
using namespace std;
// {
void print(string a) { cout << a; }
bool isalpha_case(char a) { return (isalpha(a) or (a == '_')); }
bool isalnum_case(char a) { return (isalnum(a) or (a == '_')); }
//}

// Lexer
// {
// This kind of lexer returns char values [0-255] if unknown to the grammar, negative if known
token_num = 0; // keep track of tokens
class Token
{
public:
    string str;
    int ch; // for case jumps

    Token(string name) { str=name; ch=(--token_num); }

    // make easy to print
    friend ostream& operator<<(ostream& os, const Token_base& tb)
    {
        os << tb.str;
        return os;
    }
};



/*
    
    // end of file
    _eof = -1;

    _identifier = -2;
    _number = -3;

    // recursive type
    _struct = -4;

    // base types
    _bool = -5;
    _char = -7;
    _int = -8;
    _float = -9;
    _double = -10;
    _short = -11;
    _long = -12;
    _signed = -13;
    _unsigned = -14;

    _return = -15;
*/

class Scan
{


};

// lexer portion
//// skips: whitespace, comments
queue<int> scan(string input)
{
    queue<int> tokens;
    for(int i = 0 ; i < input.length() ; i++)
    {
        // whitespace
        while(isspace(input[i]) and i < input.length())
        {
            i++;
        }

        // comments, or division
        if(i < input.length() - 1) // able to look ahead
        {
            // multiline comment
            if(input[i] == '/' and input[i + 1] == '*')
            {
                while(i < input.length() and
                        not(input[i - 1] == '*' and input[i] == '/'))
                {
                    i++;
                }
                i++;
            }

            // Comment until end of line.
            if(input[i] == '/' and input[i + 1] == '/')
            {
                do
                {
                    i++;
                }
                while(i < input.length() and
                        input[i] != '\n' and input[i] != '\r');
            }
        }


        // Identifier: [_<letter>][_<letter>0-9]+
        string IdentifierStr;
        IdentifierStr = "";
        if(isalpha_case(input[i]))
        {
            // compile name
            while(isalnum_case(input[i]))
            {
                IdentifierStr += input[i];
                i++;
            }

            //cout << IdentifierStr; exit(0);
            if(IdentifierStr == "struct")
            {
                tokens.push(token_struct);
            }
            else if(IdentifierStr == "bool")
            {
                tokens.push(token_bool);
            }
            else if(IdentifierStr == "char")
            {
                tokens.push(token_char);
            }
            else if(IdentifierStr == "int")
            {
                tokens.push(token_int);
            }
            else if(IdentifierStr == "float")
            {
                tokens.push(token_float);
            }
            else if(IdentifierStr == "double")
            {
                tokens.push(token_double);
            }
            else if(IdentifierStr == "short")
            {
                tokens.push(token_short);
            }
            else if(IdentifierStr == "long")
            {
                tokens.push(token_long);
            }
            else if(IdentifierStr == "signed")
            {
                tokens.push(token_signed);
            }
            else if(IdentifierStr == "unsigned")
            {
                tokens.push(token_unsigned);
            }
            else if(IdentifierStr == "return")
            {
                tokens.push(token_return);
            }
            else
            {
                tokens.push(token_identifier);
            }
        }

        /*
        // Number: [0-9.]+
        if(isdigit(input[i])) //or input[i] == '.')
        {
            string NumStr;
            do
            {
                NumStr += input[i];
                input[i] = getchar();
            }
            while(isdigit(input[i]) or input[i] == '.');

            NumVal = strtod(NumStr.c_str(), nullptr);
            return token_number;
        }
        */


        // what remains
        if(i >= 0 and not isspace(input[i]))
        {
            tokens.push(input[i]);
        }

        // return char if it is not recognized
    }
    return tokens;
}

void print_scanner(queue<int> q)
{
    while(not q.empty())
    {
        if(q.front() >= 0)
        {
            cout << (char) q.front();
        }
        else
        {
            switch(q.front())
            {
            case token_identifier:
                cout << "identifier ";
                break;
            case token_number:
                cout << "number ";
                break;
            case token_struct:
                cout << "struct ";
                break;
            case token_bool:
                cout << "bool ";
                break;
            case token_char:
                cout << "char ";
                break;
            case token_int:
                cout << "int ";
                break;
            case token_float:
                cout << "float ";
                break;
            case token_double:
                cout << "double ";
                break;
            case token_short:
                cout << "short ";
                break;
            case token_long:
                cout << "long ";
                break;
            case token_signed:
                cout << "signed ";
                break;
            case token_unsigned:
                cout << "unsigned ";
                break;
            case token_return:
                cout << "return ";
                break;
            }
        }
        q.pop();
    }
}

// }


struct SourceLocation
{
    int line;
    int col;
};

// Parse Expr*
// {
// default character, or list of them
// denoted _
class Tree_base
{
    SourceLocation sl; 

public:
    string name = "";
    int getLine() const { return sl.line; }
    int getCol() const { return sl.col; }

};

// one of the primitives, like int
//struct Primitive { string type; }

// recursive structure
// structAST := struct name { body } ;
//  body     := _ | LeafstructAST _ | structAST _
struct Struct
{
    string name;
    Expr* body;

    virtual 
};



// }

// Parser
// {
Expr* parse(queue<int> tokens)
{
    // the program
    Expr* program = new Expr;
    

    int token;

    // make the AST
    while(not tokens.empty())
    {
        token = tokens.front();
        tokens.pop();
        switch(token)
        {
        case token_struct:
            
            break;
        default: // language element not recoqnized
            last = to_ret;
            to_ret->name += token;
        }
    }
    return to_ret;
}
// }

// Expr* ops
// {
Expr* tree_ops(Expr* tree)
{
    return tree;
}
// }

// Code gen
// {
// Read . Eval . Print . Loop
void print_tree(Expr* tree)
{
    if(tree != NULL)
    {
        print(tree->name);
        print_tree(tree->next);
    }
}

// }
#include <fstream>

int main(int argc, char** argv)
{
    string file_name = argv[1];
    string data = "";

    fstream newfile;
    newfile.open(file_name, ios::in);
    if(newfile.is_open())
    {
        string tp;
        while(getline(newfile, tp))
        {
            data += tp;
            data += "\n";
        }
        newfile.close();
    }

    print("just data\n");
    print(data);

    print("\nscanner: \n");
    print_scanner(scan(data));

    print("\nfull processing: \n");
    print_tree(tree_ops(parse(scan(data))));

    return 0;
}

