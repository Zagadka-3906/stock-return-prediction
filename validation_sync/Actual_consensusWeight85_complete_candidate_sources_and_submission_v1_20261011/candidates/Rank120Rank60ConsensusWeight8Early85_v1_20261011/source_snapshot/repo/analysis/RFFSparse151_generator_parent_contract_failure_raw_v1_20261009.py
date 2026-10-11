"""Generate151 canonical routes before quality; materialize only the admitted sealed selection."""
from pathlib import Path
import ast,sys,hashlib,time,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import prepare_HuberSparse59_round150_sources_v2_20261009 as original

def route(s):
    s=s.replace('prepare_HuberSparse59_round150_sources_v2_20261009','prepare_RFFSparse59_round151_sources_v1_20261009')
    s=s.replace('HuberSparse150_storage_v1_20261008','RFFSparse151_storage_v2_20261009')
    s=s.replace('HuberSparse','RFFSparse').replace('RFFSparse150','RFFSparse151').replace('round150','round151').replace('_r150','_r151')
    s=re.sub(r'(RFFSparse[A-Za-z0-9_/-]*?)_v1_20261008',r'\1_v1_20261009',s)
    s=re.sub(r'(RFFSparse[A-Za-z0-9_]*)_20261008',r'\1_20261009',s)
    s=s.replace('round151_v2_20261008','round151_v2_20261009').replace('round151_qa61_20261007','round151_qa62_20261009')
    s=s.replace('qa_v61_20261007','qa_v62_20261009').replace('qa_v{qa_version}_20261007','qa_v{qa_version}_20261009')
    s=s.replace('wave433','wave434').replace('QA61','QA62').replace('第150轮','第151轮')
    s=s.replace('146、147、148、149四个合格锚点','147、148、149、150四个合格锚点')
    s=s.replace('Huber与稀疏残差组合','RFF与稀疏残差组合').replace('72原生/72冷检查','90原生/90冷检查')
    s=s.replace('登记第151轮94项跨模型完整方案','登记第151轮59项RFF与稀疏残差完整方案')
    return s

NAMES={name:route(name) for name in original.NAMES.values()}

def source_paths():
    names=[
        'RFFSparse59_round151_plan_v1_20261009.json','RFFSparse59_round151_proposal_v1_20261009.json',
        'RFFSparse151_storage_v2_20261009.py','verify_RFFSparse151_D_scoring_scope_v2_20261009.py','RFFSparse151_D_scoring_scope_v1_20261009.json',
        'RFFSparse_complete_parent_CDF_v3_20261009.py','RFFSparse_complete_parent_native_stage_v3_20261009.py',
        'predict_RFFSparse_complete_parent_scheme_v1_20261009.py','RFFSparse151_complete_native_predictor_preparation_v1_20261009.json',
        'run_RFFSparse59_official_comparison_v3_20261009.py','prepare_RFFSparse59_selected_candidate_v3_20261009.py',
        'seal_RFFSparse59_selected_candidate_v3_20261009.py','run_RFFSparse59_round151_full_registration_v3_20261009.py',
        'RFFSparse151_core_receiver_draft_preparation_v2_20261009.json','RFFSparse151_receiver_label_refinement_v3_20261009.json',
        'prepare_RFFSparse151_receiver_label_refinement_v3_20261009.py','RFFSparse151_draft_control_bindings_v1_20261009.json',
        'RFFSparse59_synthetic55_and_state20_metadata_v1_20261009.json','actual_RFFSparse72_native_calendar_location_v1_20261009.json',
        'actual_RFFSparse55_parent134_location_v1_20261009.json','actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json',
        'sparse150151_all20_annual_native_coverage_v1_20261009.json','verify_sparse150151_all20_annual_native_coverage_v1_20261009.py',
        'verify_RFFSparse59_prospective_routes_v1_20261009.py','RFFSparse59_prospective_routes_v1_20261009.json',
        'verify_RFFSparse59_round151_sources_v1_20261009.py','publish_RFFSparse59_evidence_v1_20261009.py',
        'verify_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        'actual_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.json','RFFSparse151_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json',
        'RFFSparse59_actual_controls_index_v1_20261009.json','RFFSparse59_round151_source_admission_v1_20261009.json',
        'RFFSparse59_round151_source_preparation_v1_20261009.json','RFFSparse59_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
        'RFFSparse59_scores_github_v1_20261009/receipt.json','short_content_addressed_native_storage_v2_20261008.py',
        'verified_TLS_Git_retry_runtime_v2_20261008.py','resolve_sealed_scientific_protocol_v2_20261007.py',
        'nonflag_residual_RFF128_codec_20261007.py','nonflag_sparse_Gram64_codec_20261007.py']
    # Existing generation ancestors are preserved as source dependencies, not invoked for quality or inference.
    ancestors=[Path(original.__file__),Path(original.original.__file__),Path(original.original.original.__file__),
        A/'prepare_HuberSparse150_core_receiver_drafts_v2_20261008.py',A/'prepare_HuberSparse150_complete_receiver_refinement_v3_20261009.py']
    pointer=A/'actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json'
    supplemental=Path(read(pointer)['output'])/'verification.json'
    return list(dict.fromkeys([Path(__file__),*ancestors,*(A/n for n in names),*(A/n for n in NAMES.values()),supplemental]))

def generate(parent):
    assert parent in (147,148,149,150)
    previous=parent if parent<150 else 149
    result={}
    for old,text in original.generate(previous).items():
        name=route(old);text=route(text)
        if parent!=previous:
            text=text.replace('_r149/', '_r150/').replace("'analysis/optimization_20261003_r149'","'analysis/optimization_20261003_r150'")
            text=text.replace('PREVIOUS_NUMBER = 149','PREVIOUS_NUMBER = 150').replace("'explicit_parent_round': 149","'explicit_parent_round': 150").replace('explicit_comparison_parent_round=149','explicit_comparison_parent_round=150')
        # These numeric constants are round/QA/wave contracts in registry and presentation adapters.
        class Contracts(ast.NodeTransformer):
            def visit_Constant(self,node):
                if type(node.value) is int and node.value in (150,61,433):node.value={150:151,61:62,433:434}[node.value]
                return node
        tree=Contracts().visit(ast.parse(text));text=ast.unparse(ast.fix_missing_locations(tree))+'\n'
        compile(text,str(A/name),'exec');result[name]=text
    assert len(result)==8
    return result

def main():
    ready_path=A/'RFFSparse59_selected_release_v1_20261009/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual59_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'RFFSparse59_official_comparison_v1_20261009/verification.json');assert len(pilot['records'])==59 and pilot['best']==ready['best']
    admission=A/'RFFSparse59_round151_source_admission_v1_20261009.json';proof=read(admission)
    assert proof['complete32_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    assert proof['all20_own_annual_native_states_replayed']
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,source in generated.items():assert not (A/name).exists() and hashlib.sha256(source.encode()).hexdigest()==expected[name]
    for name,source in generated.items():(A/name).write_text(source,encoding='utf8',newline='\n')
    create(A/'RFFSparse59_round151_source_preparation_v1_20261009.json',{'status':'passed_actual59_sealed_candidate_and_admitted_full151_QA62_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
