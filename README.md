# Coq verified software toolchain unfinished features

## Overall Project Milestones

-  casting between integers and pointers.

    * May be able to change the axioms and create abstraction layer.

    * Characterizes direct memory access "int* ptr = 10;" 
    
        + Sound may not automatically mean safe in this case

        + Could include a way to give a safe memory map with C code

-  goto statements.

    * parses at least, does not recognize loop tactics

-  structured switch statements (Duff's device).

    * Could be done in theory I think (without performance cost)

    * Or the optimization technique could be ignored and turned into a simple for loop

-   struct-copying assignments, struct parameters, or struct returns.

    * working on desugaring for AST (using VST tools, or by preprocessing)
        + leaves behind a mess
    
    * Reasoning About Recursive Tree Traversals' RETREET?



