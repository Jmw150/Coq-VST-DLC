struct struct_name{ int struct_element_name; float flo;};struct bigger_struct{ struct struct_name s_obj;};int main (){ struct struct_name object_name1; struct struct_name object_name2; object_name2 = object_name1; object_name2.struct_element_name = object_name1.struct_element_name; return 0;}

[
'{\'STRUCTDEF\':
    {\'ID\':\'struct_name\',
     \'BODY\':
        ["{\'BASETYPE\':
            {\'TYPE\':\'INT\',
             \'ID\':\'struct_element_name\'}}",
         "{\'BASETYPE\':
            {\'TYPE\':\'FLOAT\',
             \'ID\':\'flo\'}}"]}}', 
'{\'STRUCTDEF\':
    {\'ID\':\'bigger_struct\',
     \'BODY\':
        ["{\'STRUCTINIT\':
            {\'TYPE\':\'struct_name\',\'ID\':\'struct_name\'}}"]}}', 
        
'int', 'main', '(', ')', '{', 
    "{'STRUCTINIT':
        {'TYPE':'struct_name',
         'ID':'struct_name'}}", 
    "{'STRUCTINIT':{'TYPE':'struct_name','ID':'struct_name'}}", 

    "{'ID':'object_name2'}", '=', "{'ID':'object_name1'}", ';', 

"{'ID':'object_name2'}", '.', "{'ID':'struct_element_name'}", '=', "{'ID':'object_name1'}", '.', "{'ID':'struct_element_name'}", ';', 'return', '0', ';', '}']

{'struct_name': {'STRUCTDEF': {'ID': 'struct_name', 'BODY': ["{'BASETYPE':{'TYPE':'INT','ID':'struct_element_name'}}", "{'BASETYPE':{'TYPE':'FLOAT','ID':'flo'}}"]}}, 'bigger_struct': {'STRUCTDEF': {'ID': 'bigger_struct', 'BODY': ["{'STRUCTINIT':{'TYPE':'struct_name','ID':'struct_name'}}"]}}}

['{\'STRUCTDEF\':{\'ID\':\'struct_name\',\'BODY\':["{\'BASETYPE\':{\'TYPE\':\'INT\',\'ID\':\'struct_element_name\'}}", "{\'BASETYPE\':{\'TYPE\':\'FLOAT\',\'ID\':\'flo\'}}"]}}', '{\'STRUCTDEF\':{\'ID\':\'bigger_struct\',\'BODY\':["{\'STRUCTINIT\':{\'TYPE\':\'struct_name\',\'ID\':\'struct_name\'}}"]}}', 'int', 'main', '(', ')', '{', "{'STRUCTINIT':{'TYPE':'struct_name','ID':'struct_name'}}", "{'STRUCTINIT':{'TYPE':'struct_name','ID':'struct_name'}}", "{'ID':'object_name2'}", '=', "{'ID':'object_name1'}", ';', "{'ID':'object_name2'}", '.', "{'ID':'struct_element_name'}", '=', "{'ID':'object_name1'}", '.', "{'ID':'struct_element_name'}", ';', 'return', '0', ';', '}']