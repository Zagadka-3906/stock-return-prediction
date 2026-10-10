"""Freeze eight complete registration and original-six-view routes for six comparison parents."""
from pathlib import Path
import sys,ast,hashlib,time,io,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16TwoSeed154_core_drafts_v1_20261009 import route,replace,NAMES as COMPONENTS
import prepare_BF16Medium78_round153_sources_v1_20261009 as previous
NAMES={old:route(new) for old,new in previous.NAMES.items()}
def source_paths():
    names=['BF16TwoSeed79_round154_plan_v1_20261009.json','BF16TwoSeed79_round154_proposal_v1_20261009.json',
        'BF16TwoSeed79_synthetic73_cold219_v1_20261009.json','BF16TwoSeed154_storage_v1_20261009.py',
        'verify_BF16TwoSeed154_D_scoring_scope_v1_20261009.py','BF16TwoSeed154_D_scoring_scope_v1_20261009.json',
        'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py','BF16_complete_parent_rank_CDF_v1_20261008.py',
        'BF16TwoSeed154_complete_parent_native_stage_v1_20261009.py','predict_BF16TwoSeed154_complete_parent_scheme_v1_20261009.py',
        'verify_BF16TwoSeed154_predictor_ABI_v1_20261009.py','BF16TwoSeed154_complete_native_predictor_preparation_v1_20261009.json',
        'run_BF16TwoSeed79_official_comparison_v1_20261009.py','prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py',
        'seal_BF16TwoSeed79_selected_candidate_v1_20261009.py','run_BF16TwoSeed79_round154_full_registration_v1_20261009.py',
        'BF16TwoSeed154_core_draft_preparation_v1_20261009.json','prepare_BF16TwoSeed154_core_drafts_v1_20261009.py',
        'verify_BF16TwoSeed79_prospective_routes_v2_20261009.py','BF16TwoSeed79_prospective_routes_v1_20261009.json',
        'verify_BF16TwoSeed79_round154_sources_v1_20261009.py','BF16TwoSeed79_round154_source_admission_v1_20261009.json',
        'BF16TwoSeed79_actual_controls_index_v1_20261009.json','BF16TwoSeed79_round154_source_preparation_v1_20261009.json',
        'BF16TwoSeed79_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
        'publish_BF16TwoSeed79_evidence_v1_20261009.py','BF16TwoSeed79_scores_github_v1_20261009/receipt.json',
        'BF16TwoSeed154_actual_receiver_bindings_v1_20261009.json','prepare_BF16TwoSeed154_prospective_receivers_v1_20261009.py',
        'verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        'actual_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.json',
        'actual_BF16TwoSeed154_equal_mean_full5_location_v1_20261009.json',
        'actual_BF16TwoSeed154_native42_calendar_location_v1_20261009.json','actual_BF16TwoSeed154_full73_training_location_v1_20261009.json',
        'lossless_chunked_safe_main_runtime_v1_20261009.py','lossless_chunked_safe_main_runtime_v1_20261009.json',
        'serial_main_publication_mutex_v1_20261009.py','serial_main_publication_mutex_v1_20261009.json',
        'verified_TLS_Git_retry_runtime_v2_20261008.py','short_content_addressed_native_storage_v2_20261008.py',
        'resolve_sealed_scientific_protocol_v2_20261007.py','publish_explicit_parent_training_round_v2_20261005.py']
    for seed in ('09','10'):
        names.extend([f'neural_BF16_medium2048_seed{seed}_e64_frontier_v1_20261009.json',
            f'neural_BF16_medium2048_seed{seed}_e64_native_v1_20261009.py',
            f'neural_BF16_medium2048_seed{seed}_independent_forward_v1_20261009.py',
            f'actual_BF16_medium2048_seed{seed}_e64_bank6_location_v1_20261009.json'])
    return list(dict.fromkeys([Path(__file__),Path(previous.__file__),*(A/n for n in names),*(A/n for n in NAMES.values())]))
def generate(parent):
    assert parent in range(148,154)
    # Extend only the old generator's comparison-parent assertion in memory.
    text=Path(previous.__file__).read_text(encoding='utf8')
    text=replace(text,'assert parent in (148,149,150,151,152);result={}',
        'assert parent in (148,149,150,151,152,153);result={}')
    namespace={'__file__':previous.__file__,'__name__':'unmodified153_generator_extended_comparison_parent_only'}
    exec(compile(text,previous.__file__,'exec'),namespace)
    result={}
    for name,text in namespace['generate'](parent).items():
        name=route(name);s=route(text)
        # These eight registration/QA programs contain no training epoch constants.
        s=tokenize.untokenize([t._replace(string='65') if t.type==tokenize.NUMBER and t.string=='64' else t for t in tokenize.generate_tokens(io.StringIO(s).readline)])
        s=s.replace('第138轮','第154轮')
        # A153 comparison parent shares the predecessor's target number: bind
        # comparison fields explicitly after target routing, never infer them
        # from a round-number substitution.
        replacements=[]
        tree=ast.parse(s)
        for node in ast.walk(tree):
            value=None
            if isinstance(node,ast.Assign):
                ids=[t.id for t in node.targets if isinstance(t,ast.Name)]
                if 'comparison_baseline' in ids:value=f"read(A/'optimization_20261003_r{parent}/selection.json')['winner']['metrics']['final_score']"
                elif 'PREVIOUS' in ids:value=f"ROOT/'analysis/optimization_20261003_r{parent}'"
                elif 'PREVIOUS_NUMBER' in ids:value=str(parent)
                if value is not None:replacements.append((node.value,value))
            if isinstance(node,ast.keyword) and node.arg in ('explicit_comparison_parent_round','explicit_parent_round'):
                replacements.append((node.value,str(parent)))
            if isinstance(node,ast.Dict):
                for key,val in zip(node.keys,node.values):
                    if isinstance(key,ast.Constant) and key.value=='explicit_parent_round':replacements.append((val,str(parent)))
                    if isinstance(key,ast.Constant) and key.value=='saved_selected_parent_models':
                        replacements.append((val,f"len(read(ROOT/'candidates/optimization_20261003_r{parent}/verification.json')['models'])"))
        for node,value in sorted(replacements,key=lambda item:(item[0].lineno,item[0].col_offset),reverse=True):
            s=previous.replace_node(s,node,value)
        if name.startswith('register_'):
            s=replace(s,"measured['ordered_native_components']==[cfg['model']]",f"measured['ordered_native_components']=={COMPONENTS!r}")
            s=replace(s,"'first2020_active':True,'position':'after_complete_qualified_parent','sign':cfg['sign'],'invalid_signal_bits_preserved':True,",
                "'first2020_active':True,'position':'after_complete_qualified_parent','sign':cfg['sign'],'invalid_signal_bits_preserved':True,\n                    'seed_weights':[.5,.5],'seed_values':[20261009,20261010],\n                    'ordered_native_component_names':"+repr(COMPONENTS)+",")
            s=s.replace("'existing_BF16_wide_native_bank_fits': 6","'existing_BF16_wide_native_bank_fits': 12").replace('actual6_BF16_wide','actual12_BF16_wide')
            s=s.replace('valid_reversed_neural_day_average_rank_over_N','valid_signed_equal_two_seed_mean_day_average_rank_over_N')
            s=replace(s,'source.relative_to(ROOT)',"(source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))")
        if name.startswith('publish_'):
            s=replace(s,"path.relative_to(ROOT)).as_posix()", "(path.relative_to(ROOT) if path.is_relative_to(ROOT) else Path('external_metadata')/(sha(path)+'_'+path.name))).as_posix()")
            s=replace(s,"path.relative_to(ROOT).as_posix()] = raw_sha", "(path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path))] = raw_sha")
            start=s.index("    payload[(prefix/'README.md').as_posix()] += (");end=s.index('    previous = ',start)
            s=s[:start]+"    payload[(prefix/'README.md').as_posix()] += ('\\n第154轮：六个合格比较锚点加73种双种子等权融合，共79项。固定完整148为新阶段基底，两个独立种子共12年度模型；全5635800行均值、42原生/42冷、73历史/219截断检查均指向实际记录。选优遵循连续官方S、物理模型数、绝对权重及case。原六视图QA65，main；测试标签未读取，未证明穷尽。\\n').encode('utf8')\n"+s[end:]
        compile(s,str(A/name),'exec');result[name]=s
    assert len(result)==8 and set(result)==set(NAMES.values())
    return result
def main():
    ready_path=A/'BF16TwoSeed79_selected_release_v1_20261009/selected_candidate_ready_for_registration.json';ready=read(ready_path)
    assert ready['status']=='passed_actual79_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot=read(A/'BF16TwoSeed79_official_comparison_v1_20261009/verification.json');assert len(pilot['records'])==79 and pilot['best']==ready['best']
    admission=A/'BF16TwoSeed79_round154_source_admission_v1_20261009.json';proof=read(admission)
    assert proof['complete48_routes_and_graph_controls_passed'] and proof['prior_complete_forecast_duplicate_audit_passed']
    for f,d in proof['input_sha256'].items():assert sha(f)==d,f
    generated=generate(pilot['actual_comparison_parent_round']);expected=proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])]
    for name,s in generated.items():assert not (A/name).exists() and hashlib.sha256(s.encode()).hexdigest()==expected[name]
    for name,s in generated.items():(A/name).write_text(s,encoding='utf8',newline='\n')
    create(A/'BF16TwoSeed79_round154_source_preparation_v1_20261009.json',{
        'status':'passed_actual79_sealed_candidate_and_admitted_full154_QA65_sources',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_comparison_parent_round':pilot['actual_comparison_parent_round'],
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),ready_path,admission,*(A/n for n in generated)]},'new_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
