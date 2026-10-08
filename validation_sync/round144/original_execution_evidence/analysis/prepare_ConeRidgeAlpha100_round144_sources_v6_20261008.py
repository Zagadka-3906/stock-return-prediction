from pathlib import Path
import hashlib,time
import prepare_ConeRidgeAlpha100_round144_sources_v4_20261008 as original
from run_dependency_queue_v3_20261006 import read,sha,create
ROOT=original.ROOT;A=original.A;NAMES=original.NAMES
ROUTES={'ConeRidgeAlpha100_selected_release_v1_20261008': 'ConeRidgeAlpha100_selected_release_v3_20261008', 'ConeRidgeAlpha100_v1_20261008': 'ConeRidgeAlpha100_v3_20261008', 'ConeRidgeAlpha144_storage_v3_20261008': 'ConeRidgeAlpha144_storage_v5_20261008', 'prepare_ConeRidgeAlpha100_round144_sources_v4_20261008': 'prepare_ConeRidgeAlpha100_round144_sources_v6_20261008', 'ConeRidgeAlpha100_round144_source_admission_v4_20261008': 'ConeRidgeAlpha100_round144_source_admission_v6_20261008', 'ConeRidgeAlpha100_round144_source_preparation_v4_20261008': 'ConeRidgeAlpha100_round144_source_preparation_v6_20261008', 'ConeRidgeAlpha100_scores_github_v1_20261008': 'ConeRidgeAlpha100_scores_github_v2_20261008'}
def routed(text):
    for before,after in ROUTES.items():text=text.replace(before,after)
    return text
def generate(parent):
    values={name:routed(text) for name,text in original.generate(parent).items()}
    for name,text in values.items():
        assert 'ConeRidgeAlpha100_selected_release_v1_20261008' not in text and 'ConeRidgeAlpha100_selected_release_v2_20261008' not in text,name
        compile(text,name,'exec')
    return values
def source_paths():
    paths=[Path(routed(str(p))) for p in original.source_paths()]
    extra=[Path(__file__),A/'recover144_fresh_selected_scoring_and_source_routes_v2_20261008.py',A/'short_content_addressed_native_storage_v1_20261008.py',A/'prepare_ConeRidgeAlpha100_selected_candidate_v8_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v8_20261008.py',A/'run_ConeRidgeAlpha100_round144_full_registration_v9_20261008.py',A/'connected_API_full_round_transport_v1_20261008.py']
    for name in ('ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008'):
        folder=A/'service_owned_workflows_20261006'/name;extra.extend(folder.glob('*.json'));extra.extend(folder.glob('*.log'))
    return list(dict.fromkeys([*paths,*extra]))
def main():
    ready_path=A/'ConeRidgeAlpha100_selected_release_v3_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual100_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'ConeRidgeAlpha100_official_comparison_v5_20261008/verification.json');assert len(pilot['records'])==100 and pilot['best']==ready['best']
    proof_path=A/'ConeRidgeAlpha100_round144_source_admission_v6_20261008.json';proof=read(proof_path)
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    generated=generate(pilot['actual_comparison_parent_round'])
    for name,text in generated.items():
        assert not (A/name).exists() and hashlib.sha256(text.encode()).hexdigest()==proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name],name
    for name,text in generated.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'ConeRidgeAlpha100_round144_source_preparation_v6_20261008.json',{'status':'passed_actual100_sealed_candidate_and_admitted_full144_QA55_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':144,'scored_records':100,'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/name for name in generated]]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
