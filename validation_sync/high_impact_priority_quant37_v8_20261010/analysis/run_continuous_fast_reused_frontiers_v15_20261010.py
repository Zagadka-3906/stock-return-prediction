"""Continue chronological, fully qualified train-only frontiers until the user's actual deadline."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,itertools,traceback
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from handoff_ready_goss_full_execution_20261006 import start_service
from build_reused_neural_frontier_v9_20261010 import build
OUT=A/'continuous_fast_reused_frontiers_v15_20261010'

def allowed():
    control=read(A/'current_user_runtime_control_20261010.json')
    return control['status']=='optimization_active_after_explicit_manual_resume' and datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while allowed():
        if (folder/'service_execution.json').is_file() and (folder/'native_launch.json').is_file() and not owned(read(folder/'native_launch.json')):
            result=read(folder/'service_execution.json');assert result['status']=='passed',(name,result)
            return True
        time.sleep(10)
    return False

def launch_frontier(value):
    n=value['round'];count=value['count'];tag=value['tag'];quality=f'{tag}Quality{count}';stage=tag+'Stage';full=tag+'Full17'
    wrapper=A/'manual_resume_service_alias_runtime_v5_20261010.py';aliases=A/'manual_resume_service_aliases_v2_20261010.json'
    specs=[
        (full+'_actual_full_training_controls_v1_20261009',value['full17_driver'],[]),
        (stage+'_actual_native14_calendar_v1_20261009',value['native14_driver'],[]),
        (quality+f'_round{n}_source_admission_v1_20261009',f'verify_{quality}_round{n}_sources_v1_20261010.py',[]),
        (quality+'_controls_main_publication_v1_20261009',f'publish_{quality}_evidence_v1_20261009.py',['controls']),
        (quality+'_official_comparison_v3_20261009',f'run_{quality}_official_comparison_v3_20261009.py',[]),
        (quality+'_scores_main_publication_v1_20261009',f'publish_{quality}_evidence_v1_20261009.py',['scores']),
        (quality+'_selected_candidate_preparation_v1_20261009',f'prepare_{quality}_selected_candidate_v1_20261009.py',[]),
        (quality+'_selected_candidate_sealing_v1_20261009',f'seal_{quality}_selected_candidate_v1_20261009.py',[]),
        (quality+f'_round{n}_full_registration_v1_20261009',f'run_{stage}_safe_registration_v1_20261010.py',[]),
    ]
    rows={}
    for name,driver,arguments in specs:
        assert allowed()
        path=A/driver;assert path.is_file()
        if driver.startswith('seal_'):
            corrected=A/driver.replace('_selected_candidate_v1_20261009.py','_selected_candidate_cold80_v2_20261010.py')
            if corrected.is_file():path=corrected
        if driver.startswith('publish_'):
            corrected=A/driver.replace('_evidence_v1_20261009.py','_evidence_v2_20261010.py')
            if corrected.is_file():path=corrected
        if '_safe_registration_' in driver:
            corrected=A/driver.replace('_safe_registration_v1_20261010.py','_safe_registration_QApath_v3_20261010.py')
            if corrected.is_file():path=corrected
            faster=A/driver.replace('_safe_registration_v1_20261010.py','_safe_registration_QApath_v4_20261010.py')
            if faster.is_file():path=faster
            pubenc=A/driver.replace('_safe_registration_v1_20261010.py','_safe_registration_pubenc_v6_20261010.py')
            if pubenc.is_file():path=pubenc
            waitsafe=A/driver.replace('_safe_registration_v1_20261010.py','_safe_registration_pubenc_v7_20261010.py')
            if waitsafe.is_file():path=waitsafe
        args=['--driver',str(path),'--aliases',str(aliases),'--wait-for',value['predecessor'],*['--argument='+a for a in arguments]]
        pins={str(path):sha(path),str(wrapper):sha(wrapper),str(aliases):sha(aliases)}
        existing=A/'service_owned_workflows_20261006'/name
        if existing.is_dir():
            row=read(existing/'native_launch.json')
            assert owned(row) or read(existing/'service_execution.json')['status']=='passed',(name,'Existing failed workflow requires separate immutable recovery')
            rows[name]=row
        else:
            rows[name]=start_service(name,wrapper.name,args,pins)
    create(OUT/f'round{n}_actual_hidden_launches.json',{'round':n,'launches':rows,'frontier':value,
        'all_source_prospective_controls_passed':True,'new_quality_scores_by_dispatch':0})
    return specs[-1][0]


def qualify_huber():
    # Sole GPU is free of scientific consumers after actual full160; sequential new bank controls precede next round.
    assert closed('ReusedNN160Quality19_round160_full_registration_v1_20261009')
    assert closed('actual_BF16_medium2048_huber010_seed09_restart_control_v1_20261009')
    wrapper=A/'manual_resume_service_alias_runtime_v5_20261010.py';aliases=A/'manual_resume_service_aliases_v4_20261010.json'
    tasks=[
      ('BF16Huber010161_independent_small_CPU_v1_20261009','verify_BF16Huber010161_independent_small_CPU_v1_20261009.py'),
      ('actual_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009','train_neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009.py'),
      ('BF16Huber010161_independent_full5_GPU_controls_v1_20261009','verify_BF16Huber010161_full5_independent_GPU_v1_20261009.py'),
      ('BF16Huber010161_actual_native42_calendar_v1_20261009','verify_BF16Huber010161_native42_calendar_v1_20261009.py')]
    launches={}
    for name,driver in tasks:
        if not allowed():return False
        path=A/driver
        pins={str(p):sha(p) for p in (path,wrapper,aliases,A/'neural_BF16_medium2048_huber010_seed09_e64_frontier_v1_20261010.json',A/'neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009.py',A/'neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009.py')}
        folder=A/'service_owned_workflows_20261006'/name
        if folder.exists():
            launch=read(folder/'native_launch.json')
            assert owned(launch) or read(folder/'service_execution.json')['status']=='passed'
        else:
            launch=start_service(name,wrapper.name,['--driver',str(path),'--aliases',str(aliases)],pins)
        launches[name]=launch
        write(OUT/'state.json',{'status':'actual_new_rank_Huber_bank_or_independent_controls_running','round':161,'recipe':'huber010','role':'nonflag_valid','grid':10,'quality_cases':19,'QA':72,'actual_service':name,'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'new_quality_scores':0,'future_X_read':False})
        if not closed(name):return False
    bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009')
    assert read(bank/'verification.json')['actual_native_fits']==6
    full=read(Path(read(A/'actual_BF16Huber010161_full5_independent_location_v1_20261009.json')['output'])/'verification.json')
    native=read(Path(read(A/'actual_BF16Huber010161_native42_calendar_location_v1_20261009.json')['output'])/'verification.json')
    assert full['rows_days_stocks']==[5635800,1212,4650] and len(full['records'])==5
    assert native['actual_saved_states']==6 and native['actual_cold_cases']==42 and len(native['prefit_rejections'])==7
    create(OUT/'Huber010_actual_six_bank_controls_qualified.json',{'status':'passed_own_six_fits_full5_and_native42_before_any_new_quality','launches':launches,'own_complete_annual_fits':6,'no_future_X_or_test_Y':True})
    return True

def qualify_protected162():
    assert closed('ReusedNN161Quality19_round161_full_registration_v1_20261009')
    native_name='TailProtected162_selected_native14_v1_20261010'
    driver=A/'prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py'
    folder=A/'service_owned_workflows_20261006'/native_name
    if not folder.exists():
        pins={str(p):sha(p) for p in (driver,A/'protected_tail_after157_native_stage_v1_20261010.py',
            A/'predict_protected_tail_after157_complete_scheme_v1_20261010.py',
            A/'protected_tail_after157_native_predictor_preparation_v1_20261010.json')}
        row=start_service(native_name,driver.name,[],pins)
        create(OUT/'protected162_actual_native_launch.json',row)
    write(OUT/'state.json',{'status':'actual_protected_tail76_selected_native14_running_before162_future_features',
        'round':162,'recipe':'selected_protected_tail','role':'nonflag_valid','grid':'protected','quality_cases':76,'QA':73,
        'actual_service':native_name,'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'new_quality_scores_by_dispatch':0})
    if not closed(native_name):return False
    descriptor=A/'TailProtected162_full76_ready_dispatch_v1_20261010.json'
    while allowed() and not descriptor.exists():
        write(OUT/'state.json',{'status':'protected_tail_native_controls_closed_full_candidate_source_preparation_in_progress',
            'round':162,'quality_cases':76,'QA':73,'actual_service':native_name,'awaited_descriptor':str(descriptor),
            'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'future_X_read_by_controller':False})
        time.sleep(15)
    if not allowed():return False
    declaration=read(descriptor)
    assert declaration['round']==162 and declaration['quality_cases']==76 and declaration['QA']==73
    for p,d in declaration['input_sha256'].items():assert sha(p)==d,p
    target=A/declaration['driver'];name=declaration['service_name'];service=A/'service_owned_workflows_20261006'/name
    if not service.exists():
        row=start_service(name,target.name,declaration.get('arguments',[]),declaration['input_sha256'])
        create(OUT/'protected162_actual_full_family_launch.json',row)
    write(OUT/'state.json',{'status':'actual_protected_tail162_complete_candidate_and_full_ranking_qualification_running',
        'round':162,'quality_cases':76,'QA':73,'full_service':name,'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat()})
    if not closed(name):return False
    assert read(A/'optimization_20261003_r162/full_registration_execution.json')['status']=='passed'
    assert read(A/'github_validation_sync_main_20261005/round162_receipt.json')['scored_records']==76
    create(OUT/'round162_fully_qualified.json',{'status':'passed_76_protected_schemes_or_anchors_full_candidate_QA73_and_main','new_quality_scores_by_registration':0,'test_labels_read':False})
    return True

def main():
    import psutil
    OUT.mkdir(exist_ok=False)
    # First two derived contracts have already passed real prospective execution.
    create(OUT/'frozen_before_continuous_search.json',{'stop_at_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'direction_axes':{'saved_recipes':['seed09','seed10','drop05'],'new_recipe_before_quality':'Huber_delta0.1_rank_same2048_same64epochs_same_seed09','cohorts':['flag_valid','nonflag_valid','all_valid'],
            'weights':'high-impact broad grid .004 .016 .064 .125 .25 .5 .75 1 precedes refinements; train-only cumulative157 screen separately frozen'},
        'fixed_scientific_base':152,'all_future_rounds_keep152_and_latest_qualified_anchor':True,
        'new_native_fits_for_reused_frontiers':0,'scheduled_own_rank_Huber_new_native_fits':6,'future_X_only_after_full_score_selection_and_source_freeze':True,
        'official_S_is_primary_and_unique_model_count_absolute_weight_break_ties':True,
        'stop_or_wait_on_failures_and_resource_boundaries_without_false_pass':True})
    n=158;cycle=list(itertools.product(('flag_valid','nonflag_valid','all_valid'),('seed09','seed10','drop05')))
    try:
        while allowed() and n<=1000:
            if n<=160:
                grid=(n-157)//9;role,recipe=cycle[(n-157)%9]
                if n==158:recipe,role,grid='seed10','flag_valid',0
                if n==159:recipe,role,grid='drop05','flag_valid',0
            elif n<=172:
                # Prefer broad return/turnover-sensitive and structural coverage over tiny flagged adjustments.
                recipe,role=[('huber010','nonflag_valid'),('drop05','nonflag_valid'),('seed10','nonflag_valid'),
                    ('huber010','all_valid'),('seed09','all_valid'),('seed10','all_valid'),('drop05','all_valid'),
                    ('seed09','nonflag_valid'),('huber010','flag_valid'),('seed09','flag_valid'),
                    ('seed10','flag_valid'),('drop05','flag_valid')][n-161];grid=10
            else:
                expanded=list(itertools.product(('nonflag_valid','all_valid','flag_valid'),('huber010','seed09','seed10','drop05')))
                role,recipe=expanded[(n-173)%12];grid=1+(n-173)//12
            if n==161 and not qualify_huber():break
            if n==162:
                if not qualify_protected162():break
                n+=1;continue
            while allowed() and (psutil.disk_usage('D:/').free<1.5*2**30 or psutil.disk_usage('E:/').free<22*2**30):
                write(OUT/'state.json',{'status':'waiting_actual_storage_boundary','next_round':n,
                    'available_D_GiB':psutil.disk_usage('D:/').free/2**30,'available_E_GiB':psutil.disk_usage('E:/').free/2**30,
                    'completed_records_preserved':True,'actual_measured_resource_boundary':True})
                time.sleep(45)
            if not allowed():break
            path=A/f'ReusedNN{n}_prepared_frontier_v1_20261010.json'
            if path.is_file():value=read(path)
            elif n==158:
                proof=A/'ReusedNN158Quality23_prospective_routes_v2_20261010.json';p=read(proof)
                assert p['prospective_sources']==48 and len(p['graph_controls'])==456
                value={'round':158,'count':23,'QA':69,'tag':'ReusedNN158','recipe':'seed10','role':'flag_valid','grid':0,
                    'predecessor':'BF16FlagAfter15222_round157_full_registration_v1_20261009',
                    'full17_driver':'verify_ReusedNN158Full17_full_training_v1_20261009.py',
                    'native14_driver':'verify_ReusedNN158Stage_native14_calendar_v1_20261009.py',
                    'created_source_sha256':p['input_sha256'],'new_native_fits':0,'test_labels_read':False}
                create(path,value)
            else:
                # Build only after the previous round is fully qualified; no score-adaptive test data.
                prior=f'ReusedNN{n-1}Quality{23 if n-1==158 else 19}_round{n-1}_full_registration_v1_20261009'
                if not closed(prior):break
                value=build(n,recipe,role,grid);create(path,value)
            current=launch_frontier(value)
            write(OUT/'state.json',{'status':'actual_chronological_frontier_running','round':n,'recipe':recipe,'role':role,
                'grid':grid,'quality_cases':value['count'],'QA':value['QA'],'full_service':current,
                'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat()})
            if not closed(current):break
            proof=read(A/f'optimization_20261003_r{n}/full_registration_execution.json')
            assert proof['status']=='passed'
            receipt=read(A/f'github_validation_sync_main_20261005/round{n}_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified'
            create(OUT/f'round{n}_fully_qualified.json',{'status':'passed_full_quality_freeze_inference_causal_QA_and_main',
                'round':n,'receipt':receipt,'new_native_fits':0,'test_labels_read':False})
            n+=1
    except BaseException as error:
        write(OUT/'state.json',{'status':'failed_preserved_requires_immutable_recovery','round':n,'error':f'{type(error).__name__}: {error}',
            'traceback':traceback.format_exc(),'scientific_completion_not_claimed':True})
        raise
    write(OUT/'state.json',{'status':'user_deadline_or_explicit_stop_reached','last_round':n,
        'automatic_restart_enabled':False,'global_feasible_direction_exhaustion_not_claimed':True})

if __name__=='__main__':main()
