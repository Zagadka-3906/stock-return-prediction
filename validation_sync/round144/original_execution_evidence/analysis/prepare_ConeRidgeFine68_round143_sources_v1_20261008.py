"""68 declared fine-amplitude routes, with no additional native model fits."""
from pathlib import Path
import hashlib,time
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_ConeRidge52_round142_sources_v1_20261008 as original
from prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008 import adapt
ROOT=original.ROOT;A=original.A
NAMES={name:adapt(name) for name in original.NAMES.values()}
def generate(parent):return {adapt(name):adapt(text) for name,text in original.generate(parent).items()}
def source_paths():
    existing=[p for p in original.source_paths() if p.is_file()]
    current=[A/adapt(p.relative_to(A).as_posix()) for p in existing]
    current=[p for p in current if p.is_file()]
    required=[Path(__file__).name,'prepare_ConeRidgeFine68_round143_plan_controls_v4_20261008.py','ConeRidgeFine143_partial_constructor_recovery_v4_20261008.json',
        'ConeRidgeFine68_round143_plan_v1_20261008.json','ConeRidgeFine143_storage_v1_20261008.py',
        'ConeRidgeFine143_receiver_drafts_v1_20261008.json','ConeRidgeFine143_receiver_preparation_v1_20261008.json',
        'ConeRidgeFine143_D_scoring_scope_v1_20261008.json','ConeRidgeFine68_prospective_routes_v1_20261008.json',
        'ConeRidgeFine143_native_receiver_preflight_v1_20261008.json',
        'ConeRidgeFine68_actual_controls_index_v1_20261008.json','ConeRidgeFine68_round143_source_admission_v1_20261008.json',
        'ConeRidgeFine68_round143_source_preparation_v1_20261008.json',
        'ConeRidgeFine68_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',
        'ConeRidgeFine68_scores_github_v1_20261008/receipt.json','ConeRidgeFine143_historical_causal_main_v1_20261008/receipt.json']
    return list(dict.fromkeys([*existing,*current,*[A/name for name in [*required,*NAMES.values()]]]))
def main():
    ready_path=A/'ConeRidgeFine68_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual68_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'ConeRidgeFine68_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==68 and pilot['best']==ready['best']
    proof_path=A/'ConeRidgeFine68_round143_source_admission_v1_20261008.json';proof=read(proof_path)
    assert proof['status']=='passed_actual20_heads65_current_CDF195cold24hooks_and24_prospective143_sources'
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'ConeRidgeFine68_round143_source_preparation_v1_20261008.json',{
        'status':'passed_actual68_sealed_candidate_and_admitted_full143_QA54_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':143,'scored_records':68,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
