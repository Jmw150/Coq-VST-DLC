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

int t_num = 0; // keep track of tokens

class Scan
{
    class Token
    {
    public:
        string str;
        int ch; // for case jumps

        Token(string name)
        {
            str = name;
            ch = (t_num);
            t_num--;
        }
        Token(char name)
        {
            str = name;
            ch = (t_num);
            t_num--;
        }

        // make easy to print
        friend ostream& operator<<(ostream& os, const Token& tb)
        {
            os << tb.str;
            return os;
        }
    };

public:
    // should only have to name these once
    Token t_eof{"eof"};
    Token t_identifier{"identifier"};
    Token t_number{"number"};
    Token t_struct{"struct"};
    Token t_bool{"bool"};
    Token t_char{"char"};
    Token t_int{"int"};
    Token t_float{"float"};
    Token t_double{"double"};
    Token t_short{"short"};
    Token t_long{"long"};
    Token t_signed{"signed"};
    Token t_unsigned{"unsigned"};
    Token t_return{"return"};

    queue<Token> tokens;

    queue<Token> scan(string input)
    {
        // empty token list on rescans
        while(not tokens.empty())
        {
            tokens.pop();
        }

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
                    tokens.push(t_struct);
                }
                else if(IdentifierStr == "bool")
                {
                    tokens.push(t_bool);
                }
                else if(IdentifierStr == "char")
                {
                    tokens.push(t_char);
                }
                else if(IdentifierStr == "int")
                {
                    tokens.push(t_int);
                }
                else if(IdentifierStr == "float")
                {
                    tokens.push(t_float);
                }
                else if(IdentifierStr == "double")
                {
                    tokens.push(t_double);
                }
                else if(IdentifierStr == "short")
                {
                    tokens.push(t_short);
                }
                else if(IdentifierStr == "long")
                {
                    tokens.push(t_long);
                }
                else if(IdentifierStr == "signed")
                {
                    tokens.push(t_signed);
                }
                else if(IdentifierStr == "unsigned")
                {
                    tokens.push(t_unsigned);
                }
                else if(IdentifierStr == "return")
                {
                    tokens.push(t_return);
                }
                else
                {
                    Token id(IdentifierStr);
                    tokens.push(id);
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
                return t_number;
            }
            */


            // what remains
            if(i >= 0 and not isspace(input[i]))
            {
                Token temp(input[i]);
                tokens.push(input[i]);
            }

            // return char if it is not recognized
        }
        return tokens;
    }

    // print token list
    
    void print()
    {
        queue<Token> q;
        for (int i = 0 ; i < tokens.size() ; i++)
        {
            q.push(tokens.front());

            tokens.push(tokens.front());
            tokens.pop();
        }
        while(not q.empty())
        {
            if(q.front().ch >= 0)
            {
                cout << (char) q.front().str;
            }
            else
            {
                switch(q.front())
                {
                case t_identifier.ch:
                    cout << t_identifier.str();
                    break;
                case t_number.ch:
                    cout << "number ";
                    break;
                case t_struct.ch:
                    cout << "struct ";
                    break;
                case t_bool.ch:
                    cout << "bool ";
                    break;
                case t_char.ch:
                    cout << "char ";
                    break;
                case t_int.ch:
                    cout << "int ";
                    break;
                case t_float.ch:
                    cout << "float ";
                    break;
                case t_double.ch:
                    cout << "double ";
                    break;
                case t_short.ch:
                    cout << "short ";
                    break;
                case t_long.ch:
                    cout << "long ";
                    break;
                case t_signed.ch:
                    cout << "signed ";
                    break;
                case t_unsigned.ch:
                    cout << "unsigned ";
                    break;
                case t_return.ch:
                    cout << "return ";
                    break;
                }
            }
            q.pop();
        }
    }
    */


// lexer portion
//// skips: whitespace, comments

// }
};
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
    int getLine() const
    {
        return sl.line;
    }
    int getCol() const
    {
        return sl.col;
    }

};

// one of the primitives, like int
//struct Primitive { string type; }

// recursive structure
// structAST := struct name { body } ;
//  body     := _ | LeafstructAST _ | structAST _
/*
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
        case t_struct.ch:

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
*/
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

    print("just data:\n");
    print(data);

    print("\nscanner: \n");
    //print_scanner(scan(data));

    //print("\nfull processing: \n");
    //print_tree(tree_ops(parse(scan(data))));

    return 0;
}


/*

*/
