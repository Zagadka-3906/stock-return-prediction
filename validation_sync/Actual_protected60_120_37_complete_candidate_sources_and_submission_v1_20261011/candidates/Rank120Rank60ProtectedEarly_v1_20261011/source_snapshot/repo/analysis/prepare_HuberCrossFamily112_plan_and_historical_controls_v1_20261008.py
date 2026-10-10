"""Freeze an uncovered112-case Huber cross-family direction and start real CPU-only controls."""
from pathlib import Path
from copy import deepcopy
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

GROUPS=(
    ((('huber_d010',),1.),(('ridge_l001',),1.)),
    ((('huber_d010',),-1.),(('ridge_l001',),1.)),
    ((('huber_d025',),1.),(('rff_g0125',),1.)),
    ((('huber_d025',),-1.),(('rff_g0125',),1.)),
    ((('huber_d010','huber_d025'),1.),(('bayes_diagonal',),-1.)),
    ((('huber_d010','huber_d025'),-1.),(('bayes_diagonal',),-1.)),
)


def main():
    cross_path=A/'CrossFamily94_round136_plan_v1_20261008.json';huber_path=A/'Huber52_round137_receiver_contract_v1_20261008.json'
    cross,huber=read(cross_path),read(huber_path)
    heads={h:deepcopy(huber['heads'][h]) for h in ('huber_d010','huber_d025')}
    heads.update({h:deepcopy(cross['heads'][h]) for h in ('ridge_l001','rff_g0125','bayes_diagonal')})
    sources=[Path(__file__),cross_path,huber_path,A/'CrossFamily_complete_parent_CDF_v1_20261008.py',
        A/'CrossFamily_complete_parent_native_stage_v2_20261008.py',A/'verify_CrossFamily91_parent134_historical_v1_20261008.py',
        A/'verify_CrossFamily15_native_historical_hooks_v2_20261008.py',A/'nonflag_HuberIRLS64_streamed_v1_20261008.py']
    window_controls=[]
    for year in range(2021,2026):
        reference=None
        for head,row in heads.items():
            row['native_stage_state_kind']='HuberIRLS64_linear' if head.startswith('huber_') else row['state_kind']
            path=Path(row['infos'][str(year)]);info=read(path);kind=row['state_kind']
            assert info['year']==year and info['last_training_label_date']<info['exclusive_cutoff']
            assert info['last_training_label_end']<=info['exclusive_cutoff']
            metadata={key:info[key] for key in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
            if reference is None:reference=metadata
            assert metadata==reference,(head,year)
            model=Path(info['native_model_path']);state=Path(info['independent_'+kind+'_state_path'])
            assert sha(model)==info['native_model_sha256'] and sha(state)==info['independent_'+kind+'_state_sha256']
            sources += [path,model,state]
        window_controls.append({'year':year,'shared_mature_rows_and_feature_target_numeric_SHA_exact':True,'metadata':reference})
    sources += [Path(row['oof']) for row in heads.values()]
    # Keep every original arithmetic/CDF function; replace only the predeclared group constants.
    original=A/'CrossFamily_complete_parent_CDF_v1_20261008.py';text=original.read_text(encoding='utf8')
    start=text.index('HEADS = ');end=text.index('\n\ndef mixture',start)
    text=text[:start]+'HEADS = '+repr(tuple(heads))+'\nGROUPS = '+repr(GROUPS)+'\n'+text[end:]
    codec=A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py';assert not codec.exists();compile(text,str(codec),'exec');codec.write_text(text,encoding='utf8',newline='\n');sources.append(codec)
    native_source=A/'CrossFamily_complete_parent_native_stage_v2_20261008.py';text=native_source.read_text(encoding='utf8')
    text=text.replace('from CrossFamily_complete_parent_CDF_v1_20261008 import','from HuberCrossFamily_complete_parent_CDF_v1_20261008 import')
    text=text.replace("GRAPH_KEY='nonflag_CPU_CrossFamily_complete_parent_CDF'","GRAPH_KEY='nonflag_CPU_HuberCrossFamily_complete_parent_CDF'")
    needle='    from threadpoolctl import threadpool_limits';assert text.count(needle)==1
    text=text.replace(needle,"    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS,predict_native as huber_native,predict_decoded as huber_decoded\n"+needle)
    text=text.replace("native,decoded=(rff_native,rff_decoded) if kind=='random_fourier_linear' else (lin_native,lin_decoded)","native,decoded=(huber_native,huber_decoded) if kind=='HuberIRLS64_linear' else ((rff_native,rff_decoded) if kind=='random_fourier_linear' else (lin_native,lin_decoded))")
    text=text.replace("assert kind in ('linear','random_fourier_linear')","assert kind in ('linear','random_fourier_linear','HuberIRLS64_linear')")
    needle="            if head.startswith('ridge_'):";assert text.count(needle)==1
    extra="""            if head.startswith('huber_'):
                params=bundle['model'].get_params();assert params==info['parameters']==state['training_configuration']
                assert params['solver']=='fixed8192_Huber_IRLS65_normal_equations' and params['alpha']==info['training_rows']*.01
                assert all(params[key]==value for key,value in CONFIGS[info['name']].items())
            elif head.startswith('ridge_'):"""
    text=text.replace(needle,extra)
    native=A/'HuberCrossFamily_complete_parent_native_stage_v1_20261008.py';assert not native.exists();compile(text,str(native),'exec');native.write_text(text,encoding='utf8',newline='\n');sources.append(native)
    plan_path=A/'HuberCrossFamily112_round139_plan_v1_20261008.json'
    plan={'status':'frozen112_new_Huber_crossfamily_CDF_cases_before_any_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':139,'anchors':[136,137,138],
        'heads':heads,'groups':GROUPS,'shares':[.25,.5,.75],'amplitudes':[.0025,.005,.01,.025,.05,.1],
        'new_cases':[{'group':group,'share':share,'amplitude':amplitude} for group in range(6) for share in (.25,.5,.75) for amplitude in (.0025,.005,.01,.025,.05,.1)],
        'expected_scored_cases':112,'expected_transform_cases':109,'expected_cold_cases':327,
        'reused_existing_own_mature_annual_models':25,'additional_native_fits':0,'preliminary_controls_parent':134,
        'comparison_parent_selected_only_after_full138_QA49_and_main':True,
        'graph_key':'nonflag_CPU_HuberCrossFamily_complete_parent_CDF','stage_position':'after_complete_qualified_parent',
        'teacher_feature':'qualified106_current_forecast_average_rank_over_N','universe':'all_current_raw_forecasts',
        'preserve2020_flag1_and_invalid_complete_parent_forecast_bits':True,
        'saved_final_fit_year2025_used_across_all_future_calendar_years':True,
        'window_controls':window_controls,'input_sha256':{str(p):sha(p) for p in dict.fromkeys(sources)},
        'new_official_scores':0,'actual_future_X_and_Y_read':False,'selection_bias_uncorrected':True,
        'official_S_all8_no_extra_quality_gate':True,'physical_model_counts_use_unique_SHA_union':True,'global_exhaustion_claimed':False}
    assert len(plan['new_cases'])==108;create(plan_path,plan)
    source=A/'verify_CrossFamily91_parent134_historical_v1_20261008.py';text=source.read_text(encoding='utf8')
    replacements={'CrossFamily91_parent134_historical_v1_20261008':'HuberCrossFamily109_parent134_historical_v1_20261008',
        'CrossFamily_complete_parent_CDF_v1_20261008':'HuberCrossFamily_complete_parent_CDF_v1_20261008',
        'CrossFamily94_round136_plan_v1_20261008':'HuberCrossFamily112_round139_plan_v1_20261008',
        'frozen_before_actual91_full_historical_controls':'frozen_before_actual109_full_historical_controls',
        'actual_CrossFamily91_parent134_location_v1_20261008':'actual_HuberCrossFamily109_parent134_location_v1_20261008',
        'passed_actual91_full_parent134_historical_crossfamily_CDF_and273_cold_controls':'passed_actual109_parent134_Huber_crossfamily_CDF_and327_cold_controls',
        'passed_actual91_parent134_historical_controls_on_E':'passed_actual109_parent134_Huber_crossfamily_controls_on_E',
        'final136':'final139','after135_is_qualified':'after138_is_qualified','range(5)':'range(6)',
        '==91':'==109','==273':'==327',"'actual_full_cases':91":"'actual_full_cases':109","'actual_cold_cases':273":"'actual_cold_cases':327",'/91':'/109'}
    for before,after in replacements.items():text=text.replace(before,after)
    full_driver=A/'verify_HuberCrossFamily109_parent134_historical_v1_20261008.py';assert not full_driver.exists();compile(text,str(full_driver),'exec');full_driver.write_text(text,encoding='utf8',newline='\n')
    source=A/'verify_CrossFamily15_native_historical_hooks_v2_20261008.py';text=source.read_text(encoding='utf8')
    replacements={'CrossFamily91_parent134_historical_full_controls_v1_20261008':'HuberCrossFamily109_parent134_historical_controls_v1_20261008',
        'CrossFamily15_native_historical_hooks_v2_20261008':'HuberCrossFamily18_native_historical_hooks_v1_20261008',
        'CrossFamily_complete_parent_CDF_v1_20261008':'HuberCrossFamily_complete_parent_CDF_v1_20261008',
        'CrossFamily_complete_parent_native_stage_v2_20261008':'HuberCrossFamily_complete_parent_native_stage_v1_20261008',
        'CrossFamily94_round136_plan_v1_20261008':'HuberCrossFamily112_round139_plan_v1_20261008',
        'actual_CrossFamily91_parent134_location_v1_20261008':'actual_HuberCrossFamily109_parent134_location_v1_20261008',
        'actual_CrossFamily15_native_hooks_location_v2_20261008':'actual_HuberCrossFamily18_native_hooks_location_v1_20261008',
        'passed_actual15_historical_native_crossfamily_hooks_and15_cold_prefixes':'passed_actual18_Huber_crossfamily_native_historical_hooks_and18_cold_prefixes',
        'passed_actual15_historical_crossfamily_native_hooks_on_E':'passed_actual18_Huber_crossfamily_native_historical_hooks_on_E',
        'frozen_before_actual15':'frozen_before_actual18',"'groups':5":"'groups':6",'range(5)':'range(6)',
        '==91':'==109','==273':'==327',"'actual_hooks':15":"'actual_hooks':18","'actual_cold_hooks':15":"'actual_cold_hooks':18",'/15':'/18','final136':'final139'}
    for before,after in replacements.items():text=text.replace(before,after)
    needle="'name':info['name'],'state_kind':kind";assert text.count(needle)==1
    text=text.replace(needle,"'name':info['name'],'state_kind':row['native_stage_state_kind']")
    hook_driver=A/'verify_HuberCrossFamily18_native_historical_hooks_v1_20261008.py';assert not hook_driver.exists();compile(text,str(hook_driver),'exec');hook_driver.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),plan_path,codec,native,full_driver,hook_driver]}
    launches={}
    for name,driver in (('HuberCrossFamily109_parent134_historical_controls_v1_20261008',full_driver),
        ('HuberCrossFamily18_native_historical_hooks_v1_20261008',hook_driver)):
        launches[name]=start(name,driver.name,[],pins)
    create(A/'actual_HuberCrossFamily112_plan_and_historical_hidden_launches_v1_20261008.json',{
        'status':'frozen112_cases_and_started_actual109_full327cold_then18_native18cold_historical_controls',
        'input_sha256':pins,'launches':launches,'original_GPU_training_unchanged':True,'additional_native_fits':0,'new_official_scores':0,
        'complete139_source_current_parent_official_candidate_QA50_and_main_still_required':True,'test_labels_read':False})
    print('112 Huber+Ridge/RFF/Bayes cases frozen;109 full/327 cold and18 native/18 cold controls started on CPU.',flush=True)


if __name__=='__main__':main()
