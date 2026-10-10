"""Freeze25 refined CDF cases and qualified175/190 anchors for exact complete27 execution."""
from pathlib import Path
import importlib,re,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import prepare_MixedProtected190_complete39_pipeline_v1_20261011 as previous
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
FACTORY=Path(__file__).stem
PROOF='mixed_refined191_full_execution_sources_admission_v1_20261011.json'
NORMAL='normalize_completed_near_refined27_after190_v1_20261011'
QUAL='qualify_near_refined27_selected_native14_v1_20261011'
PRED='predict_three_cached_mixed_complete_qualified_parent_scheme_v2_20261011'
PLAN='near_refined_complete27_after190_plan_v1_20261011.json'
CALL='three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011.json'
STAGE='rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011'

def base(text):
    mapping={'MixedProtected190':'MixedRefined191','mixed_protected190':'mixed_refined191',
             'round190':'round191','round189':'round190','_r190':'_r191','_r189':'_r190',
             '第190轮':'第191轮','qualified189':'qualified190','qa101':'qa102','QA101':'QA102',
             'qa_v101':'qa_v102','wave473':'wave474','17726':'17753'}
    for prefix in ['complete','full','anchor','normalized','all','actual','exact','selected','pilot']:
        mapping[prefix+'39']=prefix+'27'
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    text=pattern.sub(lambda m:mapping[m.group()],text)
    return re.sub(r'(?<![A-Za-z0-9_])(190|189|473|101|39|36|108)(?![A-Za-z0-9_])',
           lambda m:{'190':'191','189':'190','473':'474','101':'102','39':'27','36':'24','108':'72'}[m.group()],text)

NAMES=[base(n) for n in previous.NAMES]
EXTRAS=[NORMAL+'.py',QUAL+'.py',*[base(n) for n in previous.EXTRAS[2:11]],PLAN,PRED+'.py',CALL,
        STAGE+'.py','near_refined27_normalization_native14_sources_admission_v1_20261011.json',
        'three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011.json',
        *[n for n in previous.EXTRAS[18:] if 'near_protected' not in n]]

def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))

def route(text):
    mapping={previous.EXTRAS[0]:NORMAL+'.py',previous.EXTRAS[1]:QUAL+'.py',previous.EXTRAS[11]:PLAN,
             previous.EXTRAS[12]:PRED+'.py',previous.EXTRAS[13]:CALL,Path(previous.__file__).name:FACTORY+'.py',
             previous.STAGE:STAGE,
             'actual_near_protected39_selected_native14_location_v1_20261011.json':'actual_near_refined27_selected_native14_location_v1_20261011.json',
             'near_protected39_selected_native14_v1_20261011':'near_refined27_selected_native14_v1_20261011',
             'MixedObjectiveWindow189_complete149_family_v3_20261011':'MixedProtected190_complete39_family_v1_20261011',
             'rank5_rank20_near_protected_complete_parent_native_replay_verification.json':'rank5_rank20_mixed_complete_parent_native_replay_verification.json',
             'passed_actual_complete175_near_protected_two_full_native_independent_scalar_mix_and_cold80':'passed_actual_complete175_mixed_horizon_two_full_native_independent_scalar_mix_and_cold80',
             'passed_selected_near_protected39_six_pairs14_native14_cold7_prefit_refusals':'passed_selected_near_refined27_six_pairs14_native14_cold7_prefit_refusals'}
    mapping.update({Path(k).stem:Path(v).stem for k,v in list(mapping.items()) if k.endswith('.py')})
    placeholders={k:'__SOURCE191_'+str(i)+'__' for i,k in enumerate(mapping)}
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    text=pattern.sub(lambda m:placeholders[m.group()],text);text=base(text)
    for k,v in placeholders.items():text=text.replace(v,mapping[k])
    text=text.replace('near_protected39','near_refined27')
    return text

def main():
    assert allowed();assert read(A/PLAN)['expected_records']==27 and len(read(A/CALL)['records'])==11
    admission=A/'near_refined27_normalization_native14_sources_admission_v1_20261011.json'
    for p,d in read(admission)['input_sha256'].items():assert sha(p)==d,p
    inputs=[A/n for n in previous.NAMES+previous.EXTRAS[2:9]];texts={}
    for source in inputs:
        text=route(source.read_text(encoding='utf8'))
        if source.name==previous.EXTRAS[3]:
            text=text.replace("cfg['stage_kind']=='rank5_rank20_mixed_raw_average_protected_tail'","cfg['stage_kind']=='rank5_rank20_mixed_raw_average'")
            text=text.replace('per-day protected parent-value permutation by independently matured Rank20/Rank5 raw average; official Top codec preserves its documented cutoff-tie treatment',
                              'per-day CDF perturbation of whole qualified175 by independently matured Rank20/Rank5 raw average')
        if source.name==previous.NAMES[0]:
            text=text.replace("['near_protected37','qualified175','qualified190']","['near_refined25','qualified175','qualified190']")
        target=A/base(source.name);assert not target.exists();compile(text,str(target),'exec');texts[target]=text
    assert 'wave474_results.json' in texts[A/NAMES[0]]
    assert '(191, 102, 27)' in texts[A/NAMES[-1]]
    assert "closed('MixedProtected190_complete39_family_v1_20261011')" in texts[A/EXTRAS[6]]
    for target,text in texts.items():target.write_text(text,encoding='utf8',newline='\n')
    aliases=[]
    for name in NAMES[2:4]:
        source=A/name;target=A/name.replace('_v1_20261011.py','.py');assert not target.exists();target.write_bytes(source.read_bytes());aliases.append(target)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(191,190,(474,))
    storage=importlib.import_module(Path(EXTRAS[2]).stem)
    assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    pins={str(p):sha(p) for p in [Path(__file__),*inputs,*texts,*aliases,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]}
    for name in EXTRAS[9:11]:create(A/name,{'status':'compiled_exact27_refined25_QA102_before_future','input_sha256':pins,'expected_records':27,'expected_full_board':17753,'parent_rounds':[175,190],'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    create(A/PROOF,{'status':'compiled_complete27_refined_two_model_CDF_replay_QA102_CPU11_before_future','input_sha256':pins,
           'expected_records':27,'expected_full_board':17753,'actual_callback_CPU_count':11,'actual_models_per_nonidentity_signal':2,
           'parent_rounds':[175,190],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert all(p.is_file() for p in source_paths())
    assert allowed();name='MixedRefined191_complete27_family_v1_20261011'
    row=start_service(name,EXTRAS[5],[],{str(A/EXTRAS[5]):sha(A/EXTRAS[5]),str(A/PROOF):sha(A/PROOF)})
    create(A/(name+'_activation.json'),row)
    print({'actual191_27_queued':True,'new_fits':0,'actual_future_and_main_pending':True},flush=True)

if __name__=='__main__':main()
