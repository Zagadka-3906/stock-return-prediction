"""Identify a bounded runtime improvement without changing the ranking builder or active validations."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'build_all_model_rankings_20261003.py';text=source.read_text(encoding='utf8');tree=ast.parse(text)
    main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    guard=next(n for n in main.body if isinstance(n,ast.If) and "validation_provenance_erratum_20261003.json" in ast.unparse(n.test))
    previous_json=next(n for n in main.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='output_json.write_text')
    repeated_json=next(n for n in guard.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='output_json.write_text')
    previous_embed=next(n for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='embedded' for t in n.targets))
    repeated_embed=next(n for n in guard.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='embedded' for t in n.targets))
    assert ast.dump(previous_json.value,include_attributes=False)==ast.dump(repeated_json.value,include_attributes=False)
    assert ast.dump(previous_embed.value,include_attributes=False)==ast.dump(repeated_embed.value,include_attributes=False)
    erratum=ROOT/'results/validation_provenance_erratum_20261003.json';assert erratum.is_file()
    proof=A/'lossless_ranking_display_qa_v47_20261007/round136/verification.json';qa=read(proof)
    assert qa['status']=='passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
    create(A/'full_board_redundant_serialization_audit_v1_20261008.json',{
        'status':'passed_actual_source_AST_identical_encode_calls_and_existing_branch_input_audit_only',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,erratum,proof]},
        'actual_complete_connected_records':qa['original_full_QA_result']['connected_records'],
        'original_pretty_write_line':previous_json.lineno,'conditional_final_pretty_write_line':repeated_json.lineno,
        'original_compact_encode_line':previous_embed.lineno,'conditional_final_compact_encode_line':repeated_embed.lineno,
        'active_erratum_branch_exists':True,'full_report_encode_calls_in_current_branch':4,
        'initial_two_results_overwritten_after_final_note_append':True,
        'proposed_optimization':'defer_the_first_pretty_and_compact_encoding_when_the_existing_erratum_branch_will_overwrite_both',
        'required_before_adoption':['isolated_new_runtime_adapter_with_original_builder_bytes_retained',
            'actual_full_board_original_vs_deferred_byte_equivalence_at_a_fixed_display_timestamp',
            'complete_original_six_view_browser_and_source_provenance_QA',
            'two_order_actual_time_and_memory_measurements',
            'freeze_new_runtime_receivers_before_use_in_a_new_validation_round'],
        'actual_runtime_speedup_not_measured':True,'actual_runtime_change_not_adopted':True,
        'active_original_builder_not_modified':True,'new_quality_scores':0,'test_labels_read':False})
    print('Source audit passed: four full encodes, initial two overwritten; full benchmark required before adoption.',flush=True)
if __name__=='__main__':main()
