from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_nonflag_Ridge40_round121_sources_v1_20261007 as original_generator
NAMES=original_generator.NAMES
CORRECTION_MAP={'run_nonflag_Ridge40_round121_full_registration_v1_20261007': 'run_nonflag_Ridge40_round121_full_registration_v2_20261007', 'verify_nonflag_Ridge40_round121_sources_v1_20261007': 'verify_nonflag_Ridge40_round121_sources_v2_20261007', 'publish_nonflag_Ridge40_evidence_v1_20261007': 'publish_nonflag_Ridge40_evidence_v2_20261007', 'prepare_nonflag_Ridge40_round121_sources_v1_20261007': 'prepare_nonflag_Ridge40_round121_sources_v2_20261007'}
def generate(parent):
    return {n:substitute(t,CORRECTION_MAP) for n,t in original_generator.generate(parent).items()}
def main():
    ready_path=A/'nonflag_Ridge40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'; ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'nonflag_Ridge40_official_comparison_v1_20261007/verification.json'); assert len(pilot['records'])==40 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round']; proof_path=A/'nonflag_Ridge40_round121_source_admission_v1_20261007.json'; proof=read(proof_path)
    assert proof['status']=='passed_actual37_controls_and24_prospective121_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_Ridge40_round121_source_preparation_v1_20261007.json',{'status':'passed_actual40_sealed_candidate_and_admitted_full121_QA32_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':121,'scored_records':40,'actual_comparison_parent_round':parent,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
