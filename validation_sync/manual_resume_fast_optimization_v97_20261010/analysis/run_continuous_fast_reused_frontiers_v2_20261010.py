"""Continue chronological, fully qualified train-only frontiers until the user's actual deadline."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,time,itertools,traceback
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from scheduled_user_pause_20261007 import write
from handoff_ready_goss_full_execution_20261006 import start_service
from build_reused_neural_frontier_v2_20261010 import build
OUT=A/'continuous_fast_reused_frontiers_v2_20261010'

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
    wrapper=A/'manual_resume_service_alias_runtime_v3_20261010.py';aliases=A/'manual_resume_service_aliases_v2_20261010.json'
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

def main():
    import psutil
    OUT.mkdir(exist_ok=False)
    # First two derived contracts have already passed real prospective execution.
    create(OUT/'frozen_before_continuous_search.json',{'stop_at_local':read(A/'current_user_runtime_control_20261010.json')['stop_at_local'],
        'direction_axes':{'saved_recipes':['seed09','seed10','drop05'],'cohorts':['flag_valid','nonflag_valid','all_valid'],
            'weights':'two coarse grids, one wide/tiny grid, then deterministic bounded refinements fixed before each new score'},
        'fixed_scientific_base':152,'all_future_rounds_keep152_and_latest_qualified_anchor':True,
        'new_native_fits':0,'future_X_only_after_full_score_selection_and_source_freeze':True,
        'official_S_is_primary_and_unique_model_count_absolute_weight_break_ties':True,
        'stop_or_wait_on_failures_and_resource_boundaries_without_false_pass':True})
    n=158;cycle=list(itertools.product(('flag_valid','nonflag_valid','all_valid'),('seed09','seed10','drop05')))
    try:
        while allowed() and n<=1000:
            grid=(n-157)//9;role,recipe=cycle[(n-157)%9]
            if n==158:recipe,role,grid='seed10','flag_valid',0
            if n==159:recipe,role,grid='drop05','flag_valid',0
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
