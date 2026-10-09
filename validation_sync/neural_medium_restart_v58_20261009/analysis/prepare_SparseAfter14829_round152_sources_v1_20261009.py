"""Generate eight complete152 registration routes for each comparison anchor, fixed scientific base148."""
from pathlib import Path
import sys,ast,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_HuberSparse59_round150_sources_v2_20261009 as previous
from prepare_SparseAfter148152_core_drafts_v1_20261009 import route
NAMES={n:route(n) for n in previous.NAMES.values()}
SCORER='run_SparseAfter14829_official_comparison_v2_20261009.py'

def source_paths():
    names=['SparseAfter14829_round152_plan_v1_20261009.json','SparseAfter14829_round152_proposal_v1_20261009.json',
      'SparseAfter148152_storage_v1_20261009.py','verify_SparseAfter148152_D_scoring_scope_v1_20261009.py',
      'SparseAfter148152_D_scoring_scope_v1_20261009.json','SparseAfter148_complete_parent_CDF_v1_20261009.py',
      'SparseAfter148_complete_parent_native_stage_v1_20261009.py','predict_SparseAfter148_complete_parent_scheme_v1_20261009.py',
      SCORER,'prepare_SparseAfter14829_selected_candidate_v2_20261009.py','seal_SparseAfter14829_selected_candidate_v2_20261009.py',
      'run_SparseAfter14829_round152_full_registration_v2_20261009.py','SparseAfter148152_core_draft_preparation_v1_20261009.json',
      'SparseAfter148152_complete_receiver_refinement_v3_20261009.json','prepare_SparseAfter148152_complete_receivers_v2_20261009.py',
      'verify_SparseAfter14829_round152_sources_v1_20261009.py','publish_SparseAfter14829_evidence_v1_20261009.py',
      'verify_SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009.py',
      'actual_SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009.json',
      'SparseAfter148152_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json','SparseAfter14829_actual_controls_index_v1_20261009.json',
      'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json','SparseAfter148152_complete_native_predictor_preparation_v1_20261009.json',
      'actual_SparseAfter14860_native_calendar_location_v1_20261009.json','actual_SparseAfter14825_parent148_location_v1_20261009.json',
      'SparseAfter14829_round152_source_admission_v1_20261009.json','SparseAfter14829_round152_source_preparation_v1_20261009.json',
      'SparseAfter14829_selected_release_v1_20261009/selected_candidate_ready_for_registration.json','SparseAfter14829_scores_github_v1_20261009/receipt.json',
      'short_content_addressed_native_storage_v2_20261008.py','verified_TLS_Git_retry_runtime_v2_20261008.py','resolve_sealed_scientific_protocol_v2_20261007.py',
      'verify_SparseAfter14829_prospective_routes_v1_20261009.py','SparseAfter14829_prospective_routes_v1_20261009.json']
    return list(dict.fromkeys([Path(__file__),Path(previous.__file__),A/'prepare_HuberSparse59_round150_sources_v1_20261008.py',
        A/'prepare_SparseAfter148152_core_drafts_v1_20261009.py',*(A/n for n in names),*(A/n for n in NAMES.values())]))

def generate(parent):
    assert parent in (148,149,150,151)
    original_parent={148:146,149:147,150:148,151:149}[parent];result={}
    for old,source in previous.generate(original_parent).items():
        name=route(old);s=route(source)
        if name.startswith('register_'):
            tree=ast.parse(s);node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
            before=ast.get_source_segment(s,node.value)
            start=sum(len(line) for line in s.splitlines(keepends=True)[:node.value.lineno-1])+node.value.col_offset
            assert s[start:start+len(before)]==before
            s=s[:start]+"read(A / "+repr(f'optimization_20261003_r{parent}/selection.json')+")[\"winner\"][\"metrics\"][\"final_score\"]"+s[start+len(before):]
        if name=='optimize_training_round152.py':
            tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS' for t in n.targets))
            before=ast.get_source_segment(s,node.value)
            start=sum(len(line) for line in s.splitlines(keepends=True)[:node.value.lineno-1])+node.value.col_offset
            assert s[start:start+len(before)]==before
            s=s[:start]+"ROOT / "+repr(f'analysis/optimization_20261003_r{parent}')+s[start+len(before):]
        s=s.replace("len(measured['ordered_native_components']) in (3,4)","len(measured['ordered_native_components']) in (1,2)")
        s=s.replace('actual20_SparseAfter148_saved_native_heads_source','actual10_SparseAfter148_saved_native_heads_source')
        compile(s,str(A/name),'exec');result[name]=s
    assert len(result)==8 and set(result)==set(NAMES.values())
    return result

def main():
    ready_path=A/'SparseAfter14829_selected_release_v1_20261009/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual29_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'SparseAfter14829_official_comparison_v1_20261009/verification.json');assert len(pilot['records'])==29 and pilot['best']==ready['best']
    admission=A/'SparseAfter14829_round152_source_admission_v1_20261009.json';proof=read(admission)
    assert proof['complete32_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,s in generated.items():assert not (A/name).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[name]
    for name,s in generated.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    create(A/'SparseAfter14829_round152_source_preparation_v1_20261009.json',{'status':'passed_actual29_sealed_candidate_and_admitted_full152_QA63_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
