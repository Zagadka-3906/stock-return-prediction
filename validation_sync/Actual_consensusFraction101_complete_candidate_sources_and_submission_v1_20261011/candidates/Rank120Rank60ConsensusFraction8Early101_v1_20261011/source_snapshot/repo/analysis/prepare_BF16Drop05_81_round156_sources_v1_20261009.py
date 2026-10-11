"""Eight original-six-view registration routes per comparison parent; fixed148 individual drop05_seed09 stage."""
from pathlib import Path
import sys,ast,hashlib,time,io,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16Drop05_156_core_drafts_v1_20261009 import route
import prepare_BF16Medium78_round153_sources_v1_20261009 as previous
NAMES={old:route(new) for old,new in previous.NAMES.items()}
def source_paths():
    names=['BF16Drop05_81_round156_plan_v1_20261009.json','BF16Drop05_81_round156_proposal_v2_20261009.json',
        'BF16Drop05_81_synthetic73_cold219_v1_20261009.json','BF16Drop05_156_storage_v1_20261009.py',
        'verify_BF16Drop05_156_D_scoring_scope_v1_20261009.py','BF16Drop05_156_D_scoring_scope_v1_20261009.json',
        'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py','BF16_complete_parent_rank_CDF_v1_20261008.py',
        'BF16Drop05_156_complete_parent_native_stage_v1_20261009.py','predict_BF16Drop05_156_complete_parent_scheme_v1_20261009.py',
        'verify_BF16Drop05_156_predictor_ABI_v1_20261009.py','BF16Drop05_156_complete_native_predictor_preparation_v1_20261009.json',
        'run_BF16Drop05_81_official_comparison_v1_20261009.py','prepare_BF16Drop05_81_selected_candidate_v1_20261009.py',
        'seal_BF16Drop05_81_selected_candidate_v1_20261009.py','run_BF16Drop05_81_round156_full_registration_v1_20261009.py',
        'BF16Drop05_156_core_draft_preparation_v1_20261009.json','prepare_BF16Drop05_156_core_drafts_v1_20261009.py',
        'prepare_BF16Drop05_156_scientific_controls_v1_20261009.py','BF16Drop05_156_scientific_controls_hidden_launches_v1_20261009.json',
        'verify_BF16Drop05_81_prospective_routes_v1_20261009.py','BF16Drop05_81_prospective_routes_v1_20261009.json',
        'verify_BF16Drop05_81_round156_sources_v1_20261009.py','BF16Drop05_81_round156_source_admission_v1_20261009.json',
        'BF16Drop05_81_actual_controls_index_v1_20261009.json','BF16Drop05_81_round156_source_preparation_v1_20261009.json',
        'BF16Drop05_81_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
        'publish_BF16Drop05_81_evidence_v1_20261009.py','BF16Drop05_81_scores_github_v1_20261009/receipt.json',
        'BF16Drop05_156_actual_receiver_bindings_v1_20261009.json','prepare_BF16Drop05_156_prospective_receivers_v1_20261009.py',
        'verify_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        'actual_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.json',
        'actual_BF16Drop05_156_full5_independent_location_v1_20261009.json',
        'actual_BF16Drop05_156_native42_calendar_location_v1_20261009.json','actual_BF16Drop05_156_full73_training_location_v1_20261009.json',
        'neural_BF16_medium2048_drop05_seed09_e64_frontier_v1_20261009.json','neural_BF16_medium2048_drop05_seed09_e64_native_v1_20261009.py',
        'neural_BF16_medium2048_drop05_seed09_independent_forward_v1_20261009.py','actual_BF16_medium2048_drop05_seed09_e64_bank6_location_v1_20261009.json',
        'lossless_chunked_safe_main_runtime_v1_20261009.py','lossless_chunked_safe_main_runtime_v1_20261009.json',
        'serial_main_publication_mutex_v1_20261009.py','serial_main_publication_mutex_v1_20261009.json',
        'verified_TLS_Git_retry_runtime_v2_20261008.py','short_content_addressed_native_storage_v2_20261008.py',
        'resolve_sealed_scientific_protocol_v2_20261007.py','publish_explicit_parent_training_round_v2_20261005.py']
    return list(dict.fromkeys([Path(__file__),Path(previous.__file__),*(A/n for n in names),*(A/n for n in NAMES.values())]))
def generate(parent):
    assert parent in range(148,156)
    text=Path(previous.__file__).read_text(encoding='utf8');needle='assert parent in (148,149,150,151,152);result={}'
    assert text.count(needle)==1;text=text.replace(needle,'assert parent in range(148,156);result={}')
    namespace={'__file__':previous.__file__,'__name__':'unchanged153_generator_with_seven_explicit_comparison_parent_routes'}
    exec(compile(text,previous.__file__,'exec'),namespace);result={}
    for name,text in namespace['generate'](parent).items():
        name=route(name);s=route(text)
        s=tokenize.untokenize([t._replace(string='67') if t.type==tokenize.NUMBER and t.string=='64' else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
        tree=ast.parse(s);replacements=[]
        for node in ast.walk(tree):
            value=None
            if isinstance(node,ast.Assign):
                ids=[t.id for t in node.targets if isinstance(t,ast.Name)]
                if 'comparison_baseline' in ids:value=f"read(A/'optimization_20261003_r{parent}/selection.json')['winner']['metrics']['final_score']"
                elif 'PREVIOUS' in ids:value=f"ROOT/'analysis/optimization_20261003_r{parent}'"
                elif 'PREVIOUS_NUMBER' in ids:value=str(parent)
                if value is not None:replacements.append((node.value,value))
            if isinstance(node,ast.keyword) and node.arg in ('explicit_comparison_parent_round','explicit_parent_round'):replacements.append((node.value,str(parent)))
            if isinstance(node,ast.Dict):
                for key,val in zip(node.keys,node.values):
                    if isinstance(key,ast.Constant) and key.value=='explicit_parent_round':replacements.append((val,str(parent)))
                    if isinstance(key,ast.Constant) and key.value=='saved_selected_parent_models':replacements.append((val,f"len(read(ROOT/'candidates/optimization_20261003_r{parent}/verification.json')['models'])"))
        for node,value in sorted(replacements,key=lambda item:(item[0].lineno,item[0].col_offset),reverse=True):s=previous.replace_node(s,node,value)
        if name.startswith('register_'):
            needle='source.relative_to(ROOT)';assert s.count(needle)==1
            s=s.replace(needle,"(source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))")
        if name.startswith('publish_'):
            s=s.replace('第138轮','第156轮')
            needle='path.relative_to(ROOT)).as_posix()';assert s.count(needle)==1
            s=s.replace(needle,"(path.relative_to(ROOT) if path.is_relative_to(ROOT) else Path('external_metadata')/(sha(path)+'_'+path.name))).as_posix()")
            needle='path.relative_to(ROOT).as_posix()] = raw_sha';assert s.count(needle)==1
            s=s.replace(needle,"(path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path))] = raw_sha")
            start=s.index("    payload[(prefix/'README.md').as_posix()] += (");end=s.index('    previous = ',start)
            s=s[:start]+"    payload[(prefix/'README.md').as_posix()] += ('\\n第156轮：单独drop05_seed09神经网络在固定完整148之后的73种正负排序融合，加八个合格锚点，共81项。复用六个独立成熟年度状态，依据实际73完整/219截断、42原生/42冷控制；连续官方S优先，物理模型数与绝对权重处理同分。完整原六视图QA67，main；测试标签未读取，未证明穷尽。\\n').encode('utf8')\n"+s[end:]
        compile(s,str(A/name),'exec');result[name]=s
    assert len(result)==8 and set(result)==set(NAMES.values());return result
def main():
    ready_path=A/'BF16Drop05_81_selected_release_v1_20261009/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual81_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16Drop05_81_official_comparison_v1_20261009/verification.json');assert len(pilot['records'])==80 and pilot['best']==ready['best']
    admission=A/'BF16Drop05_81_round156_source_admission_v1_20261009.json';proof=read(admission)
    assert proof['complete64_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    for f,d in proof['input_sha256'].items():assert sha(f)==d,f
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,s in generated.items():assert not (A/name).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[name]
    for name,s in generated.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    create(A/'BF16Drop05_81_round156_source_preparation_v1_20261009.json',{
        'status':'passed_actual81_sealed_candidate_and_admitted_full156_QA67_sources','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
