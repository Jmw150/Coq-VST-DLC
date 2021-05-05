(* adding some features listed as incomplete in Verifiable C, where they are sound in separation logic

•  casting between integers and pointers.
•  goto statements.
•  struct-copying assignments,structparameters, or structreturns.
•  less-structured switch statements (Duff ’s device).

As is, these syntax tree transformations can be used on a C programs generated Coq proof file.

*)

From Coq Require Import String List ZArith.
From compcert Require Import Coqlib Integers Floats AST Ctypes Cop Clight Clightdefs.
Local Open Scope Z_scope.
Local Open Scope string_scope.

(* 
    casting between integers and pointers

    The reason seems to be due to be in 2 parts:
    (1) logic axioms do not mix addresses and int (there are 3 separation logic types in the software: 
    (2) addressing memory by location on the machine may not be permitted

    operand rule for this in veric/Cop2.v 
    
    the separation logic lemma or axiom is probably in one of these files
./VST-master/aes/list_lemmas.v
./VST-master/aes/unused/aes_round_lemmas.v
./VST-master/aes/unused/forwarding_table_lemmas.v
./VST-master/aes/unused/mult_equiv_lemmas.v
./VST-master/concurrency/common/Compcert_lemmas.v
./VST-master/concurrency/common/dry_machine_lemmas.v
./VST-master/concurrency/common/dry_machine_step_lemmas.v
./VST-master/concurrency/common/machine_semantics_lemmas.v
./VST-master/concurrency/common/threads_lemmas.v
./VST-master/concurrency/juicy/cl_step_lemmas.v
./VST-master/concurrency/juicy/join_lemmas.v
./VST-master/concurrency/juicy/resource_decay_lemmas.v
./VST-master/concurrency/juicy/semax_simlemmas.v
./VST-master/concurrency/memory_lemmas.v
./VST-master/concurrency/memsem_lemmas.v
./VST-master/concurrency/sc_drf/compcert_threads_lemmas.v
./VST-master/examples/aggregate_type/demo2/prod_lemmas.v
./VST-master/examples/cont/client_lemmas.v
./VST-master/examples/funclistmach/lemmas.v
./VST-master/examples/funclistmach2/lemmas.v
./VST-master/examples/funclistmach3/lemmas.v
./VST-master/examples/lam_ref/lam_ref_mach_lemmas.v
./VST-master/examples/lam_ref/lam_ref_type_lemmas.v
./VST-master/floyd/assert_lemmas.v
./VST-master/floyd/call_lemmas.v
./VST-master/floyd/client_lemmas.v
./VST-master/floyd/closed_lemmas.v
./VST-master/floyd/compare_lemmas.v
./VST-master/floyd/data_at_lemmas.v
./VST-master/floyd/data_at_rec_lemmas.v
./VST-master/floyd/efield_lemmas.v
./VST-master/floyd/extcall_lemmas.v
./VST-master/floyd/forward_lemmas.v
./VST-master/floyd/for_lemmas.v
./VST-master/floyd/globals_lemmas.v
./VST-master/floyd/jmeq_lemmas.v
./VST-master/floyd/nested_field_lemmas.v
./VST-master/floyd/nested_field_re_lemmas.v
./VST-master/floyd/nested_pred_lemmas.v
./VST-master/floyd/proj_reptype_lemmas.v
./VST-master/floyd/replace_refill_reptype_lemmas.v
./VST-master/floyd/reptype_lemmas.v
./VST-master/floyd/typecheck_lemmas.v
./VST-master/floyd/val_lemmas.v
./VST-master/hmacdrbg/entropy_lemmas.v
./VST-master/hmacdrbg/HMAC_DRBG_common_lemmas.v
./VST-master/hmacdrbg/HMAC_DRBG_pure_lemmas.v
./VST-master/hmacdrbg/spec_hmac_drbg_pure_lemmas.v
./VST-master/mc_reify/app_lemmas.v
./VST-master/mc_reify/reified_ltac_lemmas.v
./VST-master/msl/join_hom_lemmas.v
./VST-master/msl/knot_lemmas.v
./VST-master/msl/ramification_lemmas.v
./VST-master/msl/rmaps_lemmas.v
./VST-master/progs/dry_mem_lemmas.v


./VST-master/sepcomp/mem_lemmas.v
./VST-master/sepcomp/semantics_lemmas.v
./VST-master/sepcomp/step_lemmas.v
./VST-master/sepcomp/submit/forward_simulations_lemmas.v
./VST-master/sepcomp/submit/mem_lemmas.v
./VST-master/sepcomp/submit/step_lemmas.v
./VST-master/sepcomp/submit_shmem/effect_simulations_lemmas.v
./VST-master/sepcomp/submit_shmem/mem_lemmas.v
./VST-master/sepcomp/submit_shmem/rg_lemmas.v

./VST-master/sha/bdo_lemmas.v
./VST-master/sha/common_lemmas.v
./VST-master/sha/general_lemmas.v
./VST-master/sha/hmac_common_lemmas.v
./VST-master/sha/hmac_pure_lemmas.v
./VST-master/sha/pure_lemmas.v
./VST-master/sha/sha_lemmas.v
./VST-master/sha/sha_padding_lemmas.v
./VST-master/sha/vst_lemmas.v
./VST-master/tweetnacl20140427/split_array_lemmas.v
./VST-master/veric/aging_lemmas.v
./VST-master/veric/assert_lemmas.v
./VST-master/veric/binop_lemmas.v
./VST-master/veric/binop_lemmas2.v
./VST-master/veric/binop_lemmas3.v
./VST-master/veric/binop_lemmas4.v
./VST-master/veric/binop_lemmas5.v
./VST-master/veric/binop_lemmas6.v
./VST-master/veric/Clight_aging_lemmas.v
./VST-master/veric/Clight_assert_lemmas.v
./VST-master/veric/Clight_lemmas.v
./VST-master/veric/environ_lemmas.v
./VST-master/veric/expr_lemmas.v
./VST-master/veric/expr_lemmas2.v
./VST-master/veric/expr_lemmas3.v
./VST-master/veric/expr_lemmas4.v
./VST-master/veric/juicy_mem_lemmas.v
./VST-master/veric/rmaps_lemmas.v
./VST-master/veric/semax_lemmas.v
./VST-master/veric/val_lemmas.v
./VST-master/veristar/clause_lemmas.v
./VST-master/veristar/spred_lemmas.v
./VST-master/wand_demo/wand_demo/bst_lemmas.v
./VST-master/wand_demo/wand_demo/list_lemmas.v
./VST-master/wand_demo/wand_demo/VST_lemmas.v
    
*)
Definition int_to_pointer (prog : Ssequence) : Ssequence :=
    match prog with
    (* move int data into int ptr *)
    | (Ssequence (Sset _ (Ecast (Econst_int (Int.repr _) tint) (tptr tint))) _)
        => (Ssequence (Sset _ ((tptr tint).repr _)) _)

    (* If pattern was not matched, move on *)
    | _ => _
    (*| (Ssequence _ (Ssequence _ _)) => (Ssequence _ _)*)
    end.

(* only a few cases work, and requires whole program analysis 

    May be better to do single translations and filter:
    - is_goto_of_tag
    - blank_goto
    - branch_swap (while keeping storage requests in table?)
*)
Definition goto_to_loop (jump_tag : string) (prog : Ssequence) : Ssequence :=
    match prog with
    (* label ahead of jump: rearrange code (leave declarations), remove jump *)
    | (Ssequence (Sgoto jump_tag) (Slabel _the_exit (Ssequence _))) =>
      (Ssequence (Ssequence _)

    (* label behind jump after condition, while loop *)

    (* If pattern was not matched, move on *)
    | (Ssequence (Ssequence _)) => (Ssequence _)
    end.

Definition struct_copy (prog : Ssequence) : Ssequence := 
    | _ => _

(* switch to entering parameters in one at a time *)
Definition struct_parameters (prog : Ssequence) : Ssequence :=
    | _ => _


Definition struct_return (prog : Ssequence) : Ssequence :=
    | _ => _
