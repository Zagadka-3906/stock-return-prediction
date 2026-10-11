"""Fresh registration9: unchanged model/grid; explicit collector contract and chronological services."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_BF16reverse40_round138_sources_v1_20261008 as original
from recover_pending137to141_registration_contracts_v13_20261008 import remap,corrected_generated
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
def source_paths():
    previous=original.source_paths()
    current=[A/remap(p.relative_to(A).as_posix()) for p in previous]
    retained=[p for p in previous if p.is_file()]
    return list(dict.fromkeys([*current,*retained,Path(__file__),A/'recover_pending137to141_registration_contracts_v13_20261008.py',A/'pending137to141_receiver_preparation_v13_20261008.json',A/'prepare_pending137to141_fresh_closed_dependencies_v13_20261008.py',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']))
def generate(parent):return corrected_generated(138,original.generate(parent))
def main():
    ready_path=A/'BF16reverse40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16reverse40_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==40 and pilot['best']==ready['best']
    proof_path=A/'BF16reverse40_round138_source_admission_v13_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual6_full5GPU37CDF111cold3hooks_and24_prospective138_sources'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'BF16reverse40_round138_source_preparation_v13_20261008.json',{'status':'passed_actual40_sealed_candidate_and_admitted_full138_QA49_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':138,'scored_records':40,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})


if __name__=='__main__':main()
