"""Freeze the protected37 comparison against actual qualified175/189, without refitting."""
from pathlib import Path
import ast, importlib, re, sys
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
import prepare_MixedObjectiveWindow189_complete149_pipeline_v3_20261011 as previous
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
FACTORY=Path(__file__).stem
PROOF='mixed_protected190_full_execution_sources_admission_v1_20261011.json'
NORMAL='normalize_completed_near_protected39_after189_v1_20261011'
QUAL='qualify_near_protected39_selected_native14_v1_20261011'
PRED='predict_near_protected_complete_qualified_parent_scheme_v1_20261011'
PLAN='near_protected_complete39_after189_plan_v1_20261011.json'
CALL='near_protected_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
STAGE='rank5_rank20_near_protected_after_qualified_parent_native_stage_v1_20261011'

def base(text):
    mapping={'MixedObjectiveWindow189':'MixedProtected190','mixed_objective_window189':'mixed_protected190',
             'round189':'round190','round188':'round189','_r189':'_r190','_r188':'_r189',
             '第189轮':'第190轮','qualified188':'qualified189','qa100':'qa101','QA100':'QA101',
             'qa_v100':'qa_v101','wave472':'wave473','17687':'17726','_v3_20261011':'_v1_20261011'}
    for prefix in ['complete','full','anchor','normalized','all','actual','exact','selected','pilot']:
        mapping[prefix+'149']=prefix+'39'
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    text=pattern.sub(lambda m:mapping[m.group()],text)
    text=re.sub(r'(?<![A-Za-z0-9_])(189|188|472|100|149|144|432)(?![A-Za-z0-9_])',
                lambda m:{'189':'190','188':'189','472':'473','100':'101','149':'39','144':'36','432':'108'}[m.group()],text)
    return text

NAMES=[base(n) for n in previous.NAMES]
EXTRAS=[NORMAL+'.py',QUAL+'.py',*[base(n) for n in previous.EXTRAS[2:11]],PLAN,PRED+'.py',CALL,
        STAGE+'.py','compute_near_protected39_selected_native14_v1_20261011.py',
        'near_protected39_normalization_native14_sources_admission_v2_20261011.json',
        'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011.json',
        *previous.EXTRAS[17:]]

def source_paths():
    return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))

def route(text):
    mapping={previous.EXTRAS[0]:NORMAL+'.py',previous.EXTRAS[1]:QUAL+'.py',previous.EXTRAS[11]:PLAN,
             previous.EXTRAS[12]:PRED+'.py',previous.EXTRAS[13]:CALL,Path(previous.__file__).name:FACTORY+'.py',
             'three_cached_mixed149_selected_native14_v1_20261011':'near_protected39_selected_native14_v1_20261011',
             'actual_three_cached_mixed149_selected_native14_location_v1_20261011.json':'actual_near_protected39_selected_native14_location_v1_20261011.json',
             'mixed_objective_window189_full_family_preflight_v2_20261011.json':'mixed_protected190_full_family_preflight_v1_20261011.json',
             'registered13_StockRank20LongEmbedding188_complete48_family_v1_20261011':'MixedObjectiveWindow189_complete149_family_v3_20261011',
             'rank5_rank20_mixed_complete_parent_native_replay_verification.json':'rank5_rank20_near_protected_complete_parent_native_replay_verification.json',
             'passed_actual_complete175_mixed_horizon_two_full_native_independent_scalar_mix_and_cold80':'passed_actual_complete175_near_protected_two_full_native_independent_scalar_mix_and_cold80',
             'passed_selected_three_cached_mixed149_six_pairs14_native14_cold7_prefit_refusals':'passed_selected_near_protected39_six_pairs14_native14_cold7_prefit_refusals'}
    mapping.update({Path(k).stem:Path(v).stem for k,v in list(mapping.items()) if k.endswith('.py')})
    placeholders={k:'__SOURCE190_'+str(i)+'__' for i,k in enumerate(mapping)}
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    text=pattern.sub(lambda m:placeholders[m.group()],text)
    text=base(text)
    for k,v in placeholders.items():text=text.replace(v,mapping[k])
    text=text.replace('three_cached_mixed149','near_protected39')
    return text

def main():
    assert allowed()
    assert read(A/PLAN)['expected_records']==39
    assert len(read(A/CALL)['records'])==11
    for p,d in read(A/'near_protected39_normalization_native14_sources_admission_v2_20261011.json')['input_sha256'].items():assert sha(p)==d,p
    inputs=[A/n for n in previous.NAMES+previous.EXTRAS[2:9]]
    texts={}
    for source in inputs:
        text=route(source.read_text(encoding='utf8'))
        if source.name==previous.EXTRAS[3]:
            old=('    import rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as cdf_stage\n'
                 '    import rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011 as near_stage\n'
                 '    import rank20_short_long_after_qualified_parent_native_stage_v1_20261011 as window_stage')
            assert text.count(old)==1
            text=text.replace(old,'    import '+STAGE+' as protected_stage')
            text=text.replace("else cdf_stage","else protected_stage")
            text=text.replace("mix_field='long504_weight' if native_stage is window_stage else 'rank5_weight'","mix_field='rank5_weight'")
            text=text.replace('Path(cdf_stage.__file__),Path(near_stage.__file__),Path(window_stage.__file__)','Path(protected_stage.__file__)')
            text=text.replace("cfg['stage_kind'] in ('rank5_rank20_mixed_raw_average','rank20_short_long_mixed_raw_average')","cfg['stage_kind']=='rank5_rank20_mixed_raw_average_protected_tail'")
            text=text.replace('per-day CDF perturbation of whole qualified175 by the independently matured two-model raw average','per-day protected parent-value permutation by independently matured Rank20/Rank5 raw average; official Top codec preserves its documented cutoff-tie treatment')
            assert 'window_stage' not in text and 'cdf_stage' not in text
        if source.name==previous.NAMES[0]:
            text=text.replace("'existing_own_cached_mixed_native_bank_fits': 18","'existing_own_cached_mixed_native_bank_fits': 12")
            text=text.replace("['mixed_horizon49','near_pure49','mixed_window49','qualified175','qualified189']","['near_protected37','qualified175','qualified189']")
        target=A/base(source.name)
        assert not target.exists(),target
        compile(text,str(target),'exec');texts[target]=text
    # Validate the entire new scope before writing or dispatching any of it.
    assert 'wave473_results.json' in texts[A/NAMES[0]]
    assert '(190, 101, 39)' in texts[A/NAMES[-1]]
    for target,text in texts.items():target.write_text(text,encoding='utf8',newline='\n')
    aliases=[]
    for filename in NAMES[2:4]:
        source=A/filename;target=A/filename.replace('_v1_20261011.py','.py')
        assert not target.exists();target.write_bytes(source.read_bytes());aliases.append(target)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(190,189,(473,))
    storage=importlib.import_module(Path(EXTRAS[2]).stem)
    assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*texts,*aliases,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]}
    for name in EXTRAS[9:11]:
        create(A/name,{'status':'compiled_exact39_protected37_QA101_before_future','input_sha256':pins,'expected_records':39,'expected_full_board':17726,'parent_rounds':[175,189],'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/PROOF,{'status':'compiled_complete39_protected_two_model_replay_QA101_CPU11_before_future','input_sha256':pins,'expected_records':39,'expected_full_board':17726,'actual_callback_CPU_count':11,'actual_models_per_nonidentity_signal':2,'parent_rounds':[175,189],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert all(p.is_file() for p in source_paths())
    assert allowed();name='MixedProtected190_complete39_family_v1_20261011'
    row=start_service(name,EXTRAS[5],[],{str(A/EXTRAS[5]):sha(A/EXTRAS[5]),str(A/PROOF):sha(A/PROOF)})
    create(A/(name+'_activation.json'),row)
    print({'actual190_39_queued':True,'new_fits':0,'actual_future_and_main_pending':True},flush=True)

if __name__=='__main__':main()
