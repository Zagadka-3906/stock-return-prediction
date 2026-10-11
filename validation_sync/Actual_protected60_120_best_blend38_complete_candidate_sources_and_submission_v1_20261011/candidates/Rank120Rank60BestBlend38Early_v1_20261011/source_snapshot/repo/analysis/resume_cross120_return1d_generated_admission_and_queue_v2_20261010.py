"""Resume only the unallocated queue after source preparation; retain all verified generated inputs."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    from prepare_cross120_recent252_return1d_own_sources_v1_20261010 import route
    proof=A/'Cross120RecentReturn252Huber050_own_bank_controls_source_admission_v1_20261010.json'
    admission=read(proof)
    assert admission['encoded_features']==120 and admission['target']=='y_ret_1d' and admission['return_target_scale']==20.
    for path,digest in admission['input_sha256'].items():assert sha(path)==digest,path
    fixture=Path(read(A/'actual_Cross120RecentReturn252Huber050_past_fixture_location_v1_20261010.json')['output'])
    assert read(fixture/'verification.json')['rows']==49153 and read(fixture/'verification.json')['last_label_end']<20191231
    original=A/'run_recent252_return_own_controls_and_training_queue_v2_20261010.py'
    text=route(original.read_text(encoding='utf8'))
    before='ReturnProtected167_selected_candidate_sealing_v1_20261010'
    assert text.count(before)==2
    text=text.replace(before,'Cross120170_selected_candidate_sealing_v1_20261010')
    path=A/route(original.name);assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    create(A/'cross120_return1d_preparation_queue_gate_two_literal_references_recovery_v2_20261010.json',{
        'status':'verified_all8_prepared_sources_and_actual49153_fixture_before_fresh_unallocated_queue_gate_repair',
        'sources_sha256':{str(p):sha(p) for p in [Path(__file__),proof,path,fixture/'verification.json']},
        'original_prototype_gate_count_expected1_actual2_recorded':True,'actual_gate_literal_references':2,
        'new_native_fits':0,'new_quality_scores':0,'scientific_source_inputs_or_case_choices_changed':False,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed();row=start_service('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010',path.name,[],{str(path):sha(path),str(proof):sha(proof)})
    create(A/'actual_cross120_recent252_return_own_controls_and_training_queue_activation_v2_20261010.json',row)
    print({'prepared_sources_and_fixture_retained_verified':True,'new_queue_worker':row['owned_worker_pid'],'GPU_waits_actual170_candidate_sealing':True},flush=True)

if __name__=='__main__':main()
