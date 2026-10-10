"""Prepare full228 registration with per-record base167/168 and four own neural recipes."""
from pathlib import Path
import sys,io,tokenize,re,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

MAP={
 'qualify_RecentReturn252_after167_selected_native14_v2_20261010':'qualify_fast_neural_frontier228_selected_native14_v1_20261010',
 'RecentReturn252_after167_selected_native14_v1_20261010':'FastNeuralFrontier169_selected_native14_v1_20261010',
 'protected_RecentReturn252_after167_native_stage_v1_20261010':'fast_neural_frontier169_native_stage_v1_20261010',
 'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010':'predict_fast_neural_frontier169_complete_scheme_v1_20261010',
 'protected_RecentReturn252_after_complete167_native_v1_20261010':'fast_neural_frontier169_after_complete_parent_native_v1_20261010',
 'actual_protected_RecentReturn252_selected_native14_location_v1_20261010':'actual_fast_neural_frontier228_selected_native14_location_v1_20261010',
 'protected_RecentReturn252_selected_native14_v1_20261010':'fast_neural_frontier228_selected_native14_v1_20261010',
 'RecentReturn252Protected168':'FastNeuralFrontier169','protected168':'frontier169',
 'round168':'round169','r168':'r169','第168':'第169',
 'v79_20261010':'v80_20261010','qa79':'qa80','QA79':'QA80','wave451':'wave452',
 'protected_tail_after167_complete_parent_native_replay_verification':'frontier169_complete_parent_native_replay_verification',
}

def route(text):
    saved={}
    for i,(old,new) in enumerate(sorted(MAP.items(),key=lambda p:-len(p[0]))):
        token=f'__FRONTIER169_ROUTE_{i}__';text=text.replace(old,token);saved[token]=new
    for token,new in saved.items():text=text.replace(token,new)
    numbers={'168':'169','67':'228','79':'80','451':'452'}
    text=tokenize.untokenize([t._replace(string=numbers.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    # Only standalone metadata count67, never digits inside hashes, dates or row counts.
    return re.sub(r'(?<!\d)67(?!\d)','228',text)

def change(text,before,after):
    assert text.count(before)==1,(before,text.count(before));return text.replace(before,after)

def main():
    assert allowed();outputs={};originals=[]
    import prepare_protected168_full_registry_sources_v1_20261010 as oldroutes
    # All prior pinned scientific files are immutable inputs.
    for name in ['protected168_storage_v2_20261010.py','prepare_protected168_selected_candidate_v4_20261010.py',
                 'seal_protected168_selected_candidate_v2_20261010.py',*oldroutes.NAMES,
                 'run_RecentReturn252Protected168_full_registration_v1_20261010.py',
                 'run_RecentReturn252Protected168_complete_family_v1_20261010.py']:
        p=A/name;originals.append(p);outputs[route(name)]=route(p.read_text(encoding='utf8'))
    # New stage has one key, while preserving old parents' distinct graph keys.
    old=A/'protected_RecentReturn252_after167_native_stage_v1_20261010.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'))
    extra=" 'recent252forward20huber050':('neural_BF16_medium2048_recent252forward20huber050_seed09_e64_native_v1_20261009','neural_BF16_medium2048_recent252forward20huber050_seed09_independent_forward_v2_20261010'),\n 'recent252forward5huber050':('neural_BF16_medium2048_recent252forward5huber050_seed09_e64_native_v1_20261009','neural_BF16_medium2048_recent252forward5huber050_seed09_independent_forward_v2_20261010'),\n 'recent252rank5huber050':('neural_BF16_medium2048_recent252rank5huber050_seed09_e64_native_v1_20261009','neural_BF16_medium2048_recent252rank5huber050_seed09_independent_forward_v2_20261010'),\n"
    text=change(text,'BACKENDS={\n','BACKENDS={\n'+extra)
    text=change(text,"spec['original_complete_parent_round']==167","spec['original_complete_parent_round'] in (167,168)")
    needle="    assert meta['training_calendar_window']==252 and meta['days']<=252"
    text=change(text,needle,needle+"\n    if native.CONFIG['label_horizon_trading_days']>1:assert meta['last_label_end']<meta['cutoff_exclusive']")
    text=change(text,"'complete_parent167_executed_before_new_stage':True","'actual_complete_parent_round':spec['original_complete_parent_round'],'complete_selected_parent_executed_before_new_stage':True")
    outputs[route(old.name)]=text
    # Dynamic parent means whole167 for fine1d or whole168 for the three new targets.
    old=A/'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'))
    text=change(text,"PARENT_FILENAME='predict_protected_Return_after163_complete_scheme_v4_20261010.py'","PARENT_FILENAMES={167:'predict_protected_Return_after163_complete_scheme_v4_20261010.py',168:'predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py'}")
    text=text.replace('PROTECTED_RECENT252_AFTER_COMPLETE167','FRONTIER169_AFTER_WHOLE_SELECTED_PARENT')
    text=change(text,"assert spec['original_complete_parent_round']==167","assert spec['original_complete_parent_round'] in PARENT_FILENAMES")
    text=change(text,"source_code=ns.ROOT/'analysis'/PARENT_FILENAME","source_code=ns.ROOT/'analysis'/PARENT_FILENAMES[spec['original_complete_parent_round']]")
    text=change(text,"intermediate=candidate/'complete167_native_wrapper_with_tail_report.json'","intermediate=candidate/'whole_selected_parent_report_before_frontier169.json'")
    # Final report is new; the entire inner168 predictor and its reports stay intact.
    outputs[route(old.name)]=text
    # Selected GPU controls reuse the actual normalized228 output without rescoring.
    old=A/'qualify_RecentReturn252_after167_selected_native14_v2_20261010.py';originals.append(old)
    text=route(old.read_text(encoding='utf8'));a=text.index('    # The existing sequential controller');b=text.index("    cfg=best['configuration']",a)
    setup="""    closed('actual_fast_neural_frontier228_normalization_queue_v1_20261010')
    import numpy as np,polars as pl
    import fast_neural_frontier169_native_stage_v1_20261010 as stage
    from normalize_predeclared_fast_neural_frontier228_v1_20261010 import RECIPES as recipes
    from run import FEATURE_FILE,feature_names,to_matrix
    original=Path(read(A/'actual_fast_neural_frontier228_location_v1_20261010.json')['output'])/'pilot228.json'
    pilot=read(original);assert len(pilot['records'])==228
    records=pilot['records'];best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    assert best==pilot['best'];pins={**pilot['input_sha256'],str(original):sha(original)}
    for source in [Path(__file__),Path(stage.__file__),A/'predict_fast_neural_frontier169_complete_scheme_v1_20261010.py',A/'fast_neural_frontier169_actual_parent_callback_CPU_controls_v1_20261010.json']:
        pins[str(source)]=sha(source)
    OUT.mkdir(exist_ok=False)
    normalized={**pilot,'status':'passed_normalized228_actual_complete_training_only_official_records','input_sha256':pins,'normalization_source':str(original),'new_quality_scores_by_normalization':0}
    create(OUT/'pilot228.json',normalized)
"""
    text=text[:a]+setup+text[b:]
    text=change(text,"parentpath=A/'optimization_20261003_r167/selected_validation.npy'","parentpath=A/f'optimization_20261003_r{cfg[\"anchor_round\"]}/selected_validation.npy'")
    text=change(text,"'original_complete_parent_round':167","'original_complete_parent_round':cfg['anchor_round']")
    outputs[route(old.name)]=text
    # Candidate freezes the actual chosen base and own selected recipe; E-only scoring.
    name='prepare_frontier169_selected_candidate_v4_20261010.py';text=outputs[name]
    text=change(text,'parent_number in (166,167)','parent_number in (167,168)')
    text=change(text,"assert parent_number==167 and 0.<cfg['weight']","assert parent_number in (167,168) and 0.<cfg['weight']")
    needle="recipes={'recent252returnhuber050':";assert text.count(needle)==1
    text=text.replace(needle,"recipes={'recent252forward20huber050':'neural_BF16_medium2048_recent252forward20huber050_seed09_e64_bank6_v1_20261009','recent252forward5huber050':'neural_BF16_medium2048_recent252forward5huber050_seed09_e64_bank6_v1_20261009','recent252rank5huber050':'neural_BF16_medium2048_recent252rank5huber050_seed09_e64_bank6_v1_20261009','recent252returnhuber050':")
    needle="own_pointer={'recent252returnhuber050':";assert text.count(needle)==1
    text=text.replace(needle,"own_pointer={'recent252forward20huber050':'actual_BF16Recent252Forward20Huber050170_full5_independent_location_v1_20261009.json','recent252forward5huber050':'actual_BF16Recent252Forward5Huber050171_full5_independent_location_v1_20261009.json','recent252rank5huber050':'actual_BF16Recent252Rank5Huber050172_full5_independent_location_v1_20261009.json','recent252returnhuber050':")
    text=change(text,"scoring=A/'FastNeuralFrontier169_D_scoring_v1_20261010/selected/scoring_validation_only'","scoring=Path('E:/赛题五_本机临时/第169轮_20261010/selected_scoring/scoring_validation_only')")
    text=change(text,"ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);assert score(ctx,selected)==best['metrics']","ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring)\n        from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed as exact_E_guard\n        with exact_E_guard(scoring,OUT/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):\n            assert score(ctx,selected)==best['metrics']")
    outputs[name]=text
    # Every nonselected graph uses its own source base, not the winner's base.
    name='register_FastNeuralFrontier169_round169_artifacts_20261010.py';text=outputs[name]
    text=change(text,"f\"candidates/optimization_20261003_r{pilot['actual_scheme_base_round']}/verification.json\"","f\"candidates/optimization_20261003_r{cfg['anchor_round']}/verification.json\"")
    text=change(text,"'position':'after_complete_qualified_parent','original_complete_parent_round':167","'position':'after_complete_qualified_parent','original_complete_parent_round':cfg['anchor_round']")
    text=change(text,"comparison_baseline = read(A/'optimization_20261003_r167/selection.json')","comparison_baseline = read(A/'optimization_20261003_r168/selection.json')")
    text=change(text,'explicit_comparison_parent_round=167','explicit_comparison_parent_round=168')
    text=change(text,"'explicit_parent_round': 167","'explicit_parent_round': 168")
    text=change(text,"ROOT/'candidates/optimization_20261003_r167/verification.json'","ROOT/f'candidates/optimization_20261003_r{pilot[\"actual_scheme_base_round\"]}/verification.json'")
    text=change(text,"'original_pre_scoring_protocols': [str(Path('E:/赛题五_本机临时/RecentReturn252_after167_high_impact65_screen_v1_20261010/frozen_before_any_new_controls_or_scores.json'))]","'original_pre_scoring_protocols': [str(Path('E:/赛题五_本机临时')/(f['stem']+'_screen_v1_20261010')/'frozen_before_any_new_controls_or_scores.json') for f in read(A/'fast_neural_frontier228_selection_plan_v1_20261010.json')['families']]")
    text=change(text,"['recent252returnhuber050','complete167','qualified166','qualified167']","['recent252returnhuber050','recent252forward20huber050','recent252forward5huber050','recent252rank5huber050','complete167','complete168','qualified167','qualified168']")
    outputs[name]=text
    name='optimize_training_round169.py';text=outputs[name]
    text=change(text,'PREVIOUS_NUMBER = 167','PREVIOUS_NUMBER = 168')
    text=change(text,"PREVIOUS = ROOT/'analysis/optimization_20261003_r167'","PREVIOUS = ROOT/'analysis/optimization_20261003_r168'")
    outputs[name]=text
    # Full publisher includes all4 raw families and the truthful per-record bases.
    name='publish_FastNeuralFrontier169_round169_full_validation_20261010.py';text=outputs[name]
    text=change(text,"for family in ('RecentReturn252_after167_high_impact65_screen_v1_20261010',):","for family in tuple(f['stem']+'_screen_v1_20261010' for f in read(A/'fast_neural_frontier228_selection_plan_v1_20261010.json')['families']):")
    a=text.index("    payload[(prefix/'README.md').as_posix()] +=");b=text.index('\n    previous =',a)
    text=text[:a]+"    payload[(prefix/'README.md').as_posix()] += ('\\n第169轮：四类TRAIN内验证共226条原始评分记录，加完整167/168两个合格锚点，共228条；222项非恒等全量控制与666项因果前缀控制。同一2020—2024连续官方评分。细调方案执行完整167，三个新目标方案执行完整168，再执行各自原生阶段。选择最高官方S；仅选中非锚点执行14次保存状态与14次冷启动控制，以及两次全量1599600推理、cold80、模型重载。原六视图QA80与GitHub main。未读取测试标签。\\n').encode('utf8')\n"+text[b:]
    outputs[name]=text
    # Preserve the proven registration/encoder/transfer scopes unchanged.
    name='run_FastNeuralFrontier169_full_registration_v1_20261010.py';text=outputs[name]
    text=change(text,"closed('ReturnProtected167_round167_full_registration_cross_volume_recovery_v4_20261010')","closed('RecentReturn252Protected168_round168_full_registration_v1_20261010')")
    text=change(text,"protocol['explicit_parent_round']==167","protocol['explicit_parent_round']==168")
    text=change(text,"'current_qualified_comparison_parent_round':167","'current_qualified_comparison_parent_round':168")
    text=text.replace('verify_FastNeuralFrontier169_full67_preflight','verify_FastNeuralFrontier169_full228_preflight')
    text=text.replace('verify_FastNeuralFrontier169_full228_preflight','verify_FastNeuralFrontier169_full228_preflight')
    text=text.replace('FastNeuralFrontier169_actual_own_bank_pointer_correction_v1_20261010.json','frontier169_candidate_sources_preparation_v2_20261010.json')
    text=text.replace("'完整167之后追加近期252日收益率网络的保护排序置换'","'四类近期目标与保护排序共228项完整验证'")
    text=text.replace('已实际完成近期252日收益率65项连接验证，加合格166/167锚点，共228条','已实际完成四类226项连接验证，加合格167/168锚点，共228条')
    outputs[name]=text
    name='run_FastNeuralFrontier169_complete_family_v1_20261010.py';text=outputs[name]
    text=text.replace('verify_FastNeuralFrontier169_full67_preflight','verify_FastNeuralFrontier169_full228_preflight')
    text=text.replace('FastNeuralFrontier169_actual_own_bank_pointer_correction_v1_20261010.json','frontier169_candidate_sources_preparation_v2_20261010.json')
    outputs[name]=text
    # Route all source paths explicitly; do not introduce a nonexistent prototype v3.
    names=[route(n) for n in oldroutes.NAMES]
    sources=[*outputs,'prepare_fast_neural_frontier169_complete228_v1_20261010.py',
        'frontier169_candidate_sources_preparation_v2_20261010.json','frontier169_full_registry_source_preparation_v1_20261010.json',
        'fast_neural_frontier169_actual_parent_callback_CPU_controls_v1_20261010.json',
        'verify_FastNeuralFrontier169_full228_preflight_v1_20261010.py',
        'normalize_predeclared_fast_neural_frontier228_v1_20261010.py','fast_neural_frontier228_selection_plan_v1_20261010.json',
        'predict_protected_Return_after163_complete_scheme_v4_20261010.py','predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010.py',
        'protected_RecentReturn252_after167_native_stage_v1_20261010.py',
        'exact_E_TRAIN_validation_cache_guard_runtime_v1_20261010.py','exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py',
        'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json','exact_E_TRAIN_validation_actual_anchor168_all8_compatibility_v1_20261010.json',
        'owned_idle_publication_wait_runtime_v1_20261010.py','lossless_chunked_safe_main_runtime_v1_20261009.py','serial_main_publication_mutex_v1_20261009.py',
        'byte_exact_ranking_stream_runtime_v1_20261010.py','byte_exact_publication_encoder_runtime_v1_20261010.py','late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py','late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json']
    sources+=['neural_BF16_medium2048_'+recipe+'_seed09_e64_native_v1_20261009.py' for recipe in ['recent252returnhuber050','recent252forward20huber050','recent252forward5huber050','recent252rank5huber050']]
    outputs['prepare_frontier169_full_registry_sources_v1_20261010.py']="from pathlib import Path\nA=Path(__file__).resolve().parent\nNAMES="+repr(names)+"\ndef source_paths():return [A/n for n in "+repr(list(dict.fromkeys(sources)))+"]\n"
    # Compile every fresh source before writing any of them.
    for name,text in outputs.items():assert not (A/name).exists(),name;compile(text,str(A/name),'exec')
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    proof={'status':'compiled_only_four_family228_parent167_168_backend4_QA80_sources_before_future_dispatch',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*[A/n for n in outputs]]},'outputs':list(outputs),
        'expected_records':228,'expected_QA':80,'comparison_parent_round':168,'actual_scheme_bases':[167,168],
        'new_native_fits':0,'new_quality_scores':0,'selected_native14_and_full_inference_not_yet_completed':True,'future_X_read':False,'test_labels_read':False}
    for name in ['frontier169_candidate_sources_preparation_v2_20261010.json','frontier169_full_registry_source_preparation_v1_20261010.json']:create(A/name,proof)
    print({'compiled_fresh_sources':len(outputs),'records':228,'formal_round':169,'selected_future_inference_not_started':True},flush=True)
if __name__=='__main__':main()
