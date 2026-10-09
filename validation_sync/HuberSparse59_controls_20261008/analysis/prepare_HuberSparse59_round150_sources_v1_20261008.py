"""Declare Sparse150 registry drafts; compilation alone is not complete prospective admission."""
from pathlib import Path
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_HuberSparse150_core_receiver_drafts_v2_20261008 import convert
import prepare_CrossFamilyFine125_round145_sources_v2_20261008 as original
NAMES={n:convert(n) for n in original.NAMES.values()}

def source_paths():
    names=['HuberSparse59_round150_plan_v1_20261008.json','HuberSparse59_round150_proposal_v1_20261008.json',
        'HuberSparse150_storage_v1_20261008.py','verify_HuberSparse150_D_scoring_scope_v1_20261008.py',
        'HuberSparse_complete_parent_CDF_v1_20261008.py','HuberSparse_complete_parent_native_stage_v1_20261008.py',
        'predict_HuberSparse_complete_parent_scheme_v1_20261008.py','run_HuberSparse59_official_comparison_v1_20261008.py',
        'prepare_HuberSparse59_selected_candidate_v1_20261008.py','seal_HuberSparse59_selected_candidate_v1_20261008.py',
        'run_HuberSparse59_round150_full_registration_v1_20261008.py','HuberSparse150_core_receiver_draft_preparation_v2_20261008.json',
        'HuberSparse150_draft_control_bindings_v1_20261008.json','HuberSparse59_synthetic55_and_state20_metadata_v1_20261008.json',
        'actual_HuberSparse72_native_calendar_location_v1_20261008.json','actual_HuberSparse55_parent134_location_v1_20261008.json',
        'HuberSparse59_round150_source_admission_v1_20261008.json','HuberSparse59_round150_source_preparation_v1_20261008.json',
        'HuberSparse59_selected_release_v1_20261008/selected_candidate_ready_for_registration.json','HuberSparse59_scores_github_v1_20261008/receipt.json',
        'short_content_addressed_native_storage_v2_20261008.py','verified_TLS_Git_retry_runtime_v2_20261008.py',
        'resolve_sealed_scientific_protocol_v2_20261007.py']
    return list(dict.fromkeys([Path(__file__),Path(original.__file__),A/'prepare_HuberSparse150_core_receiver_drafts_v2_20261008.py',
        *(A/n for n in names),*(A/n for n in NAMES.values())]))

def generate(parent):
    assert parent in (146,147,148,149)
    result={}
    for old,source in original.generate(134).items():
        name=convert(old);source=convert(source)
        source=source.replace('prepare_HuberSparse59_round150_sources_v2_20261008','prepare_HuberSparse59_round150_sources_v1_20261008')
        source=source.replace('existing_CrossFamily_saved_native_heads','existing_HuberSparse_saved_native_heads')
        source=source.replace('actual20_CrossFamily_saved_native_heads_source','actual20_HuberSparse_saved_native_heads_source')
        source=source.replace('passed_actual59_CrossFamily_complete_parent_full_official_comparisons','passed_actual59_HuberSparse_complete_parent_full_official_comparisons')
        source=source.replace('CrossFamily_complete_parent_native_replay_verification.json','HuberSparse_complete_parent_native_replay_verification.json')
        source=source.replace('len(measured[\'ordered_native_components\']) in (2,3)','len(measured[\'ordered_native_components\']) in (3,4)')
        source=source.replace('len(measured[\'ordered_native_components\']) == 2','len(measured[\'ordered_native_components\']) in (3,4)')
        source=source.replace('PREVIOUS_NUMBER = 134',f'PREVIOUS_NUMBER = {parent}')
        source=source.replace("'explicit_parent_round': 134",f"'explicit_parent_round': {parent}").replace('explicit_comparison_parent_round=134',f'explicit_comparison_parent_round={parent}')
        if name=='optimize_training_round150.py':
            tree=ast.parse(source)
            assignment=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREVIOUS' for t in x.targets))
            assert isinstance(assignment.value,ast.BinOp) and isinstance(assignment.value.right,ast.Constant)
            literal=ast.get_source_segment(source,assignment.value.right);assert source.count(literal)==1
            source=source.replace(literal,repr('analysis/optimization_20261003_r'+str(parent)))
        if name.startswith('publish_'):
            source=source.replace('134、136、141、144四个合格锚点','146、147、148、149四个合格锚点')
            source=source.replace('120项新细权重及零幅度对照','54项Huber与稀疏残差组合及零幅度对照')
            source=source.replace('121完整/363冷前缀及30原生/30冷检查','55完整/165冷前缀及72原生/72冷检查')
            source=source.replace('QA56','QA61').replace('本轮125项','本轮59项')
        compile(source,str(A/name),'exec');result[name]=source
    assert len(result)==8
    return result

def main():
    ready_path=A/'HuberSparse59_selected_release_v1_20261008/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual59_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'HuberSparse59_official_comparison_v1_20261008/verification.json');assert len(pilot['records'])==59 and pilot['best']==ready['best']
    admission=A/'HuberSparse59_round150_source_admission_v1_20261008.json';proof=read(admission)
    assert proof['complete32_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,source in generated.items():assert not (A/name).exists() and hashlib.sha256(source.encode()).hexdigest()==expected[name]
    for name,source in generated.items():(A/name).write_text(source,encoding='utf8',newline='\n')
    create(A/'HuberSparse59_round150_source_preparation_v1_20261008.json',{'status':'passed_actual59_sealed_candidate_and_admitted_full150_QA61_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
