symbol table (st)
some_int {'TYPEINIT': {'TYPE': 'int', 'ID': 'some_int'}}
some_float {'TYPEINIT': {'TYPE': 'float', 'ID': 'some_float'}}
struct_name {'TYPEDEF': {'TYPE': 'struct', 'ID': 'struct_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_element_name'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'flo'}}]}}
struct_element_name {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_element_name'}}
flo {'TYPEINIT': {'TYPE': 'float', 'ID': 'flo'}}
union_name {'TYPEDEF': {'TYPE': 'union', 'ID': 'union_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'u_int'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'u_float'}}]}}
u_int {'TYPEINIT': {'TYPE': 'int', 'ID': 'u_int'}}
u_float {'TYPEINIT': {'TYPE': 'float', 'ID': 'u_float'}}
bigger_struct {'TYPEDEF': {'TYPE': 'struct', 'ID': 'bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 's_obj'}}]}}
s_obj {'TYPEINIT': {'TYPE': 'struct_name', 'ID': 's_obj'}}
even_bigger_struct {'TYPEDEF': {'TYPE': 'struct', 'ID': 'even_bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'bigger_struct', 'ID': 'bs_obj'}}, {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_leaf'}}]}}
bs_obj {'TYPEINIT': {'TYPE': 'bigger_struct', 'ID': 'bs_obj'}}
struct_leaf {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_leaf'}}
[{'TYPEINIT': {'TYPE': 'int', 'ID': 'some_int'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'some_float'}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'struct_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_element_name'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'flo'}}]}}]
[{'TYPEINIT': {'TYPE': 'float', 'ID': 'some_float'}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'struct_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_element_name'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'flo'}}]}}, {'TYPEDEF': {'TYPE': 'union', 'ID': 'union_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'u_int'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'u_float'}}]}}]
[{'TYPEDEF': {'TYPE': 'struct', 'ID': 'struct_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_element_name'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'flo'}}]}}, {'TYPEDEF': {'TYPE': 'union', 'ID': 'union_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'u_int'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'u_float'}}]}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 's_obj'}}]}}]
[{'TYPEDEF': {'TYPE': 'union', 'ID': 'union_name', 'BODY': [{'TYPEINIT': {'TYPE': 'int', 'ID': 'u_int'}}, {'TYPEINIT': {'TYPE': 'float', 'ID': 'u_float'}}]}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 's_obj'}}]}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'even_bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'bigger_struct', 'ID': 'bs_obj'}}, {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_leaf'}}]}}]
[{'TYPEDEF': {'TYPE': 'struct', 'ID': 'bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 's_obj'}}]}}, {'TYPEDEF': {'TYPE': 'struct', 'ID': 'even_bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'bigger_struct', 'ID': 'bs_obj'}}, {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_leaf'}}]}}, {'UNKNOWN': 'int'}]
[{'TYPEDEF': {'TYPE': 'struct', 'ID': 'even_bigger_struct', 'BODY': [{'TYPEINIT': {'TYPE': 'bigger_struct', 'ID': 'bs_obj'}}, {'TYPEINIT': {'TYPE': 'int', 'ID': 'struct_leaf'}}]}}, {'UNKNOWN': 'int'}, {'UNKNOWN': 'main'}]
[{'UNKNOWN': 'int'}, {'UNKNOWN': 'main'}, {'UNKNOWN': '('}]
[{'UNKNOWN': 'main'}, {'UNKNOWN': '('}, {'UNKNOWN': ')'}]
[{'UNKNOWN': '('}, {'UNKNOWN': ')'}, {'UNKNOWN': '{'}]
[{'UNKNOWN': ')'}, {'UNKNOWN': '{'}, {'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name1'}}]
[{'UNKNOWN': '{'}, {'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name1'}}, {'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name2'}}]
[{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name1'}}, {'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name2'}}, {'ID': 'object_name2'}]
[{'TYPEINIT': {'TYPE': 'struct_name', 'ID': 'object_name2'}}, {'ID': 'object_name2'}, {'UNKNOWN': '='}]
[{'ID': 'object_name2'}, {'UNKNOWN': '='}, {'ID': 'object_name1'}]
[{'UNKNOWN': '='}, {'ID': 'object_name1'}, {'UNKNOWN': ';'}]
[{'ID': 'object_name1'}, {'UNKNOWN': ';'}, {'UNKNOWN': 'return'}]
[{'UNKNOWN': ';'}, {'UNKNOWN': 'return'}, {'UNKNOWN': '0'}]
code (c)
int some_int; float some_float; structstruct_name {int struct_element_name; float flo; }; unionunion_name {int u_int; float u_float; }; structbigger_struct {struct struct_name s_obj; }; structeven_bigger_struct {struct bigger_struct bs_obj; int struct_leaf; }; int main ( ) { struct struct_name object_name1; struct struct_name object_name2; object_name2 = object_name1 ; return 0 ; } 
