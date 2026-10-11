"""Preserve pre-score cap failures and clone fresh bounded-grid receivers; never refit or touch GPU work."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    failed_names=['HuberIRLS64_49_parent134_historical_controls_v1_20261008','HuberIRLS64_18_native_historical_hooks_v1_20261008',
        'HuberIRLS64_historical_controls_main_publication_v1_20261008','HuberIRLS64_49_current_parent_controls_v1_20261008',
        'HuberIRLS64_causal_and_handoff_main_publication_v1_20261008']
    failed_files=[]
    for name in failed_names:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        assert not owned(row) and read(folder/'service_execution.json')['status']=='failed',name
        failed_files+=list(folder.glob('*.json'))+list(folder.glob('*.log'))
    native_bank=read(A/'actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json');bank_proof=read(Path(native_bank['output'])/'verification.json')
    assert bank_proof['actual_native_fits']==10 and bank_proof['actual_official_scores']==0
    old_plan=A/'HuberIRLS64_52_round137_plan_v1_20261008.json';plan=read(old_plan);assert plan['new_quality_scores']==0
    assert not (A/'actual_HuberIRLS64_49_parent134_location_v1_20261008.json').exists()
    old_names=['HuberIRLS64_complete_parent_native_stage_v1_20261008.py','predict_HuberIRLS64_complete_parent_scheme_v1_20261008.py',
        'verify_HuberIRLS64_49_parent134_historical_v1_20261008.py','verify_HuberIRLS64_18_native_historical_hooks_v1_20261008.py',
        'verify_HuberIRLS64_49_current_parent_v1_20261008.py','publish_HuberIRLS64_historical_controls_v1_20261008.py',
        'record_actual_optimization_handoff_v5_20261008.py','publish_HuberIRLS64_causal_and_handoff_v1_20261008.py']
    names={name:name.replace('_v1_','_v2_').replace('handoff_v5_','handoff_v6_') for name in old_names}
    mapping={Path(old).stem:Path(new).stem for old,new in names.items()}
    mapping.update({name:name.replace('_v1_','_v2_') for name in failed_names})
    for prefix in ('HuberIRLS64_49_parent134_historical','HuberIRLS64_18_native_historical_hooks','HuberIRLS64_49_current_parent',
        'HuberIRLS64_49_current_parent_full','HuberIRLS64_historical_controls_main','HuberIRLS64_causal_handoff_main',
        'actual_HuberIRLS64_49_parent134_location','actual_HuberIRLS64_18_native_hooks_location',
        'actual_HuberIRLS64_49_current_parent_location','actual_HuberIRLS64_49_current_parent_full_location',
        'HuberIRLS64_52_round137_plan'):
        mapping[prefix+'_v1_20261008']=prefix+'_v2_20261008'
    mapping['actual_optimization_handoff_v5_20261008']='actual_optimization_handoff_v6_20261008'
    mapping['actual_HuberIRLS64_historical_controls_hidden_launches_v1_20261008']='actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008'
    mapping['actual_HuberIRLS64_historical_publication_and_current_parent_hidden_launch_v1_20261008']='actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008'
    generated=[];old_pins={str(p):sha(p) for p in [old_plan,*[A/name for name in old_names],*failed_files]}
    for old_name,new_name in names.items():
        source=A/old_name;text=source.read_text(encoding='utf8')
        for before,after in sorted(mapping.items(),key=lambda item:-len(item[0])):text=text.replace(before,after)
        if old_name.startswith('HuberIRLS64_complete_parent_native_stage_'):
            needle="assert 0.<spec['amplitude']<=.2";assert text.count(needle)==1;text=text.replace(needle,"assert 0.<spec['amplitude']<=.1")
        if old_name.startswith('verify_HuberIRLS64_18_native_'):
            needle='(.005,.025,.2)';assert text.count(needle)==1;text=text.replace(needle,'(.005,.025,.1)')
        if old_name.startswith('publish_HuberIRLS64_historical_'):
            needle='counts==[(49,147),(18,18)];sources=list(dict.fromkeys(sources));'
            assert text.count(needle)==1
            extra="""counts==[(49,147),(18,18)]
    recovery=A/'HuberIRLS64_amplitude_cap_receiver_recovery_v2_20261008.json'
    sources += [recovery,A/'recover_HuberIRLS64_amplitude_cap_receivers_v2_20261008.py']
    sources += [Path(path) for path in read(recovery)['preserved_failed_source_and_log_sha256']]
    sources=list(dict.fromkeys(sources));"""
            text=text.replace(needle,extra)
            text=text.replace('validation_sync/HuberIRLS64_historical_20261008','validation_sync/HuberIRLS64_historical_v2_20261008')
        if old_name.startswith('record_actual_optimization_handoff_'):
            text=text.replace('plan1 frozen','plan2 frozen').replace('receiver1 is live','receiver2 is live').replace('handoff5','handoff6').replace('交接 v5','交接 v6')
            text=text.replace("'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json'","'HuberIRLS64_historical_controls_main_v2_20261008/receipt.json'")
        if old_name.startswith('publish_HuberIRLS64_causal_and_'):
            text=text.replace('validation_sync/HuberIRLS64_causal_handoff_20261008','validation_sync/HuberIRLS64_causal_handoff_v2_20261008')
        target=A/new_name;assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');generated.append(target)
    new_plan=A/'HuberIRLS64_52_round137_plan_v2_20261008.json'
    plan.update(at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),status='frozen52_bounded_CDF_cases_after_pre_score_guard_failure',
        superseded_plan=str(old_plan),superseded_plan_sha256=sha(old_plan),maximum_amplitude=.1,
        correction_reason='Original reused CDF receiver explicitly admits amplitude<=0.1;0.2 rejected before any official score.',
        new_cases=[{'group':group,'amplitude':weight} for group in range(6) for weight in (.0025,.005,.01,.025,.05,.075,.085,.1)],
        native_model_bank_unchanged=True,new_quality_scores=0,
        input_sha256={str(p):sha(p) for p in [Path(__file__),A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',
            *generated[:2],A/'nonflag_HuberIRLS64_bank10_plan_v1_20261008.json',
            A/'CrossFamily_complete_parent_CDF_v1_20261008.py',A/'predict_CrossFamily_complete_parent_scheme_v1_20261008.py',
            A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py',A/'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py']})
    assert len(plan['new_cases'])==48 and all(0.<case['amplitude']<=.1 for case in plan['new_cases']);create(new_plan,plan)
    create(A/'HuberIRLS64_amplitude_cap_receiver_recovery_v2_20261008.json',{
        'status':'fresh_bounded_grid_and8_receivers_compiled_before_any_Huber_quality_score',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'preserved_failed_source_and_log_sha256':old_pins,
        'generated_source_sha256':{str(p):sha(p) for p in generated},'corrected_plan_sha256':sha(new_plan),
        'new_quality_scores':0,'original10_native_fits_and_saved_bank_unchanged':True,
        'original_CDF_math_and_amplitude_guard_unchanged':True,'grid_changed_before_quality_from0_2_to0_085':True,
        'original_GPU_training_not_stopped_or_restarted':True,'all_original_failures_preserved':True,'test_labels_read':False})
    pins={str(p):sha(p) for p in [Path(__file__),new_plan,*generated]};rows={}
    for old_service,old_driver in zip(failed_names,[old_names[2],old_names[3],old_names[5],old_names[4],old_names[7]]):
        service=old_service.replace('_v1_','_v2_');rows[service]=start(service,names[old_driver],[],pins)
    create(A/'actual_HuberIRLS64_bounded_pipeline_hidden_launches_v2_20261008.json',{
        'status':'started_fresh49CDF18hooks_historical_main_current_parent_and_causal_handoff_after_cap_guard',
        'launches':rows,'input_sha256':pins,'actual_quality_scores':0,'full52_official_queue_not_yet_admitted':True})
    for path,digest in old_pins.items():assert sha(path)==digest,path
    print('Preserved five pre-score failures; started fresh bounded-grid receivers without changing10 trained models or GPU work.',flush=True)


if __name__=='__main__':main()
