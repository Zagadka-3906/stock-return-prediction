from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import prepare_nonflag_HGB40_round120_sources_v2_20261007 as base
NAMES=base.NAMES
ROUTE_MAP={'run_nonflag_HGB40_official_comparison_v2_20261007': 'run_nonflag_HGB40_official_comparison_v3_20261007', 'run_nonflag_HGB40_round120_full_registration_v2_20261007': 'run_nonflag_HGB40_round120_full_registration_v3_20261007', 'run_nonflag_HGB40_admitted_comparison_v2_20261007': 'run_nonflag_HGB40_admitted_comparison_v3_20261007', 'publish_nonflag_HGB40_evidence_v2_20261007': 'publish_nonflag_HGB40_evidence_v3_20261007', 'seal_nonflag_HGB40_selected_candidate_v2_20261007': 'seal_nonflag_HGB40_selected_candidate_v3_20261007', 'prepare_nonflag_HGB40_round120_sources_v2_20261007': 'prepare_nonflag_HGB40_round120_sources_v3_20261007', 'prepare_nonflag_HGB40_selected_candidate_v2_20261007': 'prepare_nonflag_HGB40_selected_candidate_v3_20261007', 'verify_nonflag_HGB40_round120_sources_v2_20261007': 'verify_nonflag_HGB40_round120_sources_v3_20261007', 'nonflag_HGB40_round120_source_admission': 'nonflag_HGB40_round120_source_admission_v3', 'nonflag_HGB40_full37_controls_main_publication': 'nonflag_HGB40_full37_controls_main_publication_v3', 'nonflag_HGB40_official_comparison': 'nonflag_HGB40_official_comparison_v3', 'nonflag_HGB40_scores_main_publication': 'nonflag_HGB40_scores_main_publication_v3', 'nonflag_HGB40_selected_candidate_preparation': 'nonflag_HGB40_selected_candidate_preparation_v3', 'nonflag_HGB40_selected_candidate_sealing': 'nonflag_HGB40_selected_candidate_sealing_v3', 'nonflag_HGB40_round120_full_registration': 'nonflag_HGB40_round120_full_registration_v3', 'resolve_sealed_scientific_protocol_20261007': 'resolve_sealed_scientific_protocol_v2_20261007', 'nonflag_HGB40_complete_pipeline_actual_hidden_launches_20261007': 'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v3_20261007', 'nonflag_HGB40_selected_release_v2_20261007': 'nonflag_HGB40_selected_release_v3_20261007', 'nonflag_HGB40_official_comparison_v2_20261007': 'nonflag_HGB40_official_comparison_v3_20261007', 'nonflag_HGB40_pre_inference_source_freeze_v2_20261007': 'nonflag_HGB40_pre_inference_source_freeze_v3_20261007', 'nonflag_HGB40_round120_source_admission_v2_20261007': 'nonflag_HGB40_round120_source_admission_v3_20261007', 'nonflag_HGB40_round120_source_preparation_v2_20261007': 'nonflag_HGB40_round120_source_preparation_v3_20261007', 'nonflag_HGB40_round120_actual_registration_v2_20261007': 'nonflag_HGB40_round120_actual_registration_v3_20261007', 'candidates/nonflag_HGB40_v2_20261007': 'candidates/nonflag_HGB40_v3_20261007'}
def generate(parent):
    result={name:substitute(text,ROUTE_MAP) for name,text in base.generate(parent).items()}
    for name,text in list(result.items()):
        if name.startswith('collect_'):
            needle="    return namespace['collect'](number, qa_version, expected_records)"
            assert text.count(needle)==1
            text=text.replace(needle,"    from exact_native_JSON_archive_runtime_20261007 import install\n    restore=install()\n    try:return namespace['collect'](number, qa_version, expected_records)\n    finally:restore()")
        elif name.startswith('register_'):
            needle="        A / 'collect_full_lossless_round120_qa31_20261007.py',"
            assert text.count(needle)==1
            text=text.replace(needle,needle+"\n        A / 'exact_native_JSON_archive_runtime_20261007.py',\n        A / 'exact_native_pretty_JSON_archive_20261007.py',\n        A / 'exact_native_JSON_full_board_benchmark_20261007/verification.json',\n        A / 'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',")
        compile(text,str(A/name),'exec');result[name]=text
    return result
def main():
    ready_path=A/'nonflag_HGB40_selected_release_v3_20261007/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'nonflag_HGB40_official_comparison_v3_20261007/verification.json')
    assert len(pilot['records'])==40 and pilot['best']==ready['best']
    parent=pilot['actual_comparison_parent_round'];proof_path=A/'nonflag_HGB40_round120_source_admission_v3_20261007.json';proof=read(proof_path)
    assert proof['status']=='passed_actual37_controls_and24_prospective120_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(parent)
    for name,text in generated.items():
        assert not (A/name).exists(),name
        assert hashlib.sha256(text.encode('utf8')).hexdigest()==proof['generated_source_sha256'][str(parent)][name]
    preparation=A/'nonflag_HGB40_round120_source_preparation_v3_20261007.json';assert not preparation.exists()
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(preparation,{'status':'passed_actual40_sealed_candidate_and_admitted_full120_QA31_sources',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':120,'scored_records':40,'actual_comparison_parent_round':parent,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,proof_path,*[A/n for n in generated]]},
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
