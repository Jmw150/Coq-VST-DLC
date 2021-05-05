# Coq verified software toolchain unfinished features

## Current Project Milestones

- struct-copying assignments (problem: naturally recursive reasoning)

    * Make prototype in easier language (python)

        + Test: before and after transformations

    * Make Coq module to transform clight syntax tree

        + Test: before and after clight syntax trees

- struct parameters

- struct returns

## Possible Future Projects

-  casting between integers and pointers.

    * Approach: May be able to change the axioms and create abstraction layer.

    * Problem: Characterizes direct memory access "int* ptr = 10;" 
    
        + Sound may not automatically mean safe in this case

        + Solution: Could include a way to give a safe memory map with C code

-  goto statements.

    * parses at least, does not recognize loop tactics

-  structured switch statements (Duff's device).

    * Could be done in theory I think (without performance cost)

    * Or the optimization technique could be ignored and turned into a simple for loop

