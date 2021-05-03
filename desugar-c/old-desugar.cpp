// A "simple" program transformer
// C++ is too long winded with expressing computation

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

using namespace std;
// {
void print(string a) { cout << a; }
bool isalpha_case(char a) { return (isalpha(a) or (a == '_')); }
bool isalnum_case(char a) { return (isalnum(a) or (a == '_')); }
// }

// Lexer
// {
// This kind of lexer returns char values [0-255] if unknown to the grammar, negative if known

int t_num = 0; // keep track of tokens
class Tokens
{
public:
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
    
    map<string,Token> tokens;

void add(string a)
    {
        tokens[a] = Token(a);
    }

};
class Scan
{

public:
    // should only have to name these once
    Tokens tokens;
    Scan()
    {
    tokens.add("eof");
    }
    /*
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
            while(isspace(input[i]) and i < input.length()) { i++; }

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
        for(int i = 0 ; i < tokens.size() ; i++)
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
/*
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
In file included from /usr/include/c++/9/fstream:40,
                 from desugar.cpp:398:
/usr/include/c++/9/bits/codecvt.h:41:1: error: expected unqualified-id before ‘namespace’
   41 | namespace std _GLIBCXX_VISIBILITY(default)
      | ^~~~~~~~~
In file included from /usr/include/x86_64-linux-gnu/c++/9/bits/basic_file.h:40,
                 from /usr/include/c++/9/fstream:42,
                 from desugar.cpp:398:
/usr/include/x86_64-linux-gnu/c++/9/bits/c++io.h:38:1: error: expected unqualified-id before ‘namespace’
   38 | namespace std _GLIBCXX_VISIBILITY(default)
      | ^~~~~~~~~
In file included from /usr/include/c++/9/fstream:42,
                 from desugar.cpp:398:
/usr/include/x86_64-linux-gnu/c++/9/bits/basic_file.h:44:1: error: expected unqualified-id before ‘namespace’
   44 | namespace std _GLIBCXX_VISIBILITY(default)
      | ^~~~~~~~~
In file included from desugar.cpp:398:
/usr/include/c++/9/fstream:47:1: error: expected unqualified-id before ‘namespace’
   47 | namespace std _GLIBCXX_VISIBILITY(default)
      | ^~~~~~~~~
In file included from /usr/include/c++/9/fstream:1293,
                 from desugar.cpp:398:
/usr/include/c++/9/bits/fstream.tcc:43:1: error: expected unqualified-id before ‘namespace’
   43 | namespace std _GLIBCXX_VISIBILITY(default)
      | ^~~~~~~~~
desugar.cpp:428:1: error: expected ‘}’ at end of input
  428 | }
      | ^
desugar.cpp:66:1: note: to match this ‘{’
   66 | {
      | ^
desugar.cpp: In member function ‘int Scan::main(int, char**)’:
desugar.cpp:405:13: error: aggregate ‘std::fstream newfile’ has incomplete type and cannot be defined
  405 |     fstream newfile;
      |             ^~~~~~~
desugar.cpp: At global scope:
desugar.cpp:428:1: error: expected unqualified-id at end of input
  428 | }
      | ^
In file included from /usr/include/c++/9/bits/stl_map.h:63,
                 from /usr/include/c++/9/map:61,
                 from desugar.cpp:6:
/usr/include/c++/9/tuple: In instantiation of ‘std::pair<_T1, _T2>::pair(std::tuple<_Args1 ...>&, std::tuple<_Args2 ...>&, std::_Index_tuple<_Indexes1 ...>, std::_Index_tuple<_Indexes2 ...>) [with _Args1 = {const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&}; long unsigned int ..._Indexes1 = {0}; _Args2 = {}; long unsigned int ..._Indexes2 = {}; _T1 = const std::__cxx11::basic_string<char>; _T2 = Tokens::Token]’:
/usr/include/c++/9/tuple:1663:63:   required from ‘std::pair<_T1, _T2>::pair(std::piecewise_construct_t, std::tuple<_Args1 ...>, std::tuple<_Args2 ...>) [with _Args1 = {const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&}; _Args2 = {}; _T1 = const std::__cxx11::basic_string<char>; _T2 = Tokens::Token]’
/usr/include/c++/9/ext/new_allocator.h:147:4:   required from ‘void __gnu_cxx::new_allocator<_Tp>::construct(_Up*, _Args&& ...) [with _Up = std::pair<const std::__cxx11::basic_string<char>, Tokens::Token>; _Args = {const std::piecewise_construct_t&, std::tuple<const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>, std::tuple<>}; _Tp = std::_Rb_tree_node<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >]’
/usr/include/c++/9/bits/alloc_traits.h:484:4:   required from ‘static void std::allocator_traits<std::allocator<_Tp1> >::construct(std::allocator_traits<std::allocator<_Tp1> >::allocator_type&, _Up*, _Args&& ...) [with _Up = std::pair<const std::__cxx11::basic_string<char>, Tokens::Token>; _Args = {const std::piecewise_construct_t&, std::tuple<const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>, std::tuple<>}; _Tp = std::_Rb_tree_node<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::allocator_traits<std::allocator<_Tp1> >::allocator_type = std::allocator<std::_Rb_tree_node<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> > >]’
/usr/include/c++/9/bits/stl_tree.h:614:32:   required from ‘void std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_M_construct_node(std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_Link_type, _Args&& ...) [with _Args = {const std::piecewise_construct_t&, std::tuple<const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>, std::tuple<>}; _Key = std::__cxx11::basic_string<char>; _Val = std::pair<const std::__cxx11::basic_string<char>, Tokens::Token>; _KeyOfValue = std::_Select1st<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; _Compare = std::less<std::__cxx11::basic_string<char> >; _Alloc = std::allocator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_Link_type = std::_Rb_tree_node<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >*]’
/usr/include/c++/9/bits/stl_tree.h:631:4:   required from ‘std::_Rb_tree_node<_Val>* std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_M_create_node(_Args&& ...) [with _Args = {const std::piecewise_construct_t&, std::tuple<const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>, std::tuple<>}; _Key = std::__cxx11::basic_string<char>; _Val = std::pair<const std::__cxx11::basic_string<char>, Tokens::Token>; _KeyOfValue = std::_Select1st<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; _Compare = std::less<std::__cxx11::basic_string<char> >; _Alloc = std::allocator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_Link_type = std::_Rb_tree_node<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >*]’
/usr/include/c++/9/bits/stl_tree.h:2455:13:   required from ‘std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::iterator std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::_M_emplace_hint_unique(std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::const_iterator, _Args&& ...) [with _Args = {const std::piecewise_construct_t&, std::tuple<const std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&>, std::tuple<>}; _Key = std::__cxx11::basic_string<char>; _Val = std::pair<const std::__cxx11::basic_string<char>, Tokens::Token>; _KeyOfValue = std::_Select1st<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; _Compare = std::less<std::__cxx11::basic_string<char> >; _Alloc = std::allocator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::iterator = std::_Rb_tree_iterator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::_Rb_tree<_Key, _Val, _KeyOfValue, _Compare, _Alloc>::const_iterator = std::_Rb_tree_const_iterator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >]’
/usr/include/c++/9/bits/stl_map.h:499:8:   required from ‘std::map<_Key, _Tp, _Compare, _Alloc>::mapped_type& std::map<_Key, _Tp, _Compare, _Alloc>::operator[](const key_type&) [with _Key = std::__cxx11::basic_string<char>; _Tp = Tokens::Token; _Compare = std::less<std::__cxx11::basic_string<char> >; _Alloc = std::allocator<std::pair<const std::__cxx11::basic_string<char>, Tokens::Token> >; std::map<_Key, _Tp, _Compare, _Alloc>::mapped_type = Tokens::Token; std::map<_Key, _Tp, _Compare, _Alloc>::key_type = std::__cxx11::basic_string<char>]’
desugar.cpp:61:17:   required from here
/usr/include/c++/9/tuple:1674:70: error: no matching function for call to ‘Tokens::Token::Token()’
 1674 |         second(std::forward<_Args2>(std::get<_Indexes2>(__tuple2))...)
      |                                                                      ^
desugar.cpp:42:5: note: candidate: ‘Tokens::Token::Token(char)’
   42 |     Token(char name)
      |     ^~~~~
desugar.cpp:42:5: note:   candidate expects 1 argument, 0 provided
desugar.cpp:36:5: note: candidate: ‘Tokens::Token::Token(std::string)’
   36 |     Token(string name)
      |     ^~~~~
desugar.cpp:36:5: note:   candidate expects 1 argument, 0 provided
desugar.cpp:30:7: note: candidate: ‘Tokens::Token::Token(const Tokens::Token&)’
   30 | class Token
      |       ^~~~~
desugar.cpp:30:7: note:   candidate expects 1 argument, 0 provided
desugar.cpp:30:7: note: candidate: ‘Tokens::Token::Token(Tokens::Token&&)’
desugar.cpp:30:7: note:   candidate expects 1 argument, 0 provided
*/
