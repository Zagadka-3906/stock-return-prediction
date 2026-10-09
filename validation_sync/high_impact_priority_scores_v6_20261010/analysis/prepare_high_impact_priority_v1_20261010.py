"""Replace only idle dispatch/observer; freeze and launch a cumulative train-only screen."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,retire_suspended

def main():
    control=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    out=A/'high_impact_priority_handoff_v1_20261010';out.mkdir(exist_ok=False)
    builder=A/'build_reused_neural_frontier_v8_20261010.py'
    text=(A/'build_reused_neural_frontier_v7_20261010.py').read_text(encoding='utf8')
    old="    if grid==0:weights=[.001,.002,.003,.004,.006,.008,.012,.016]"
    assert text.count(old)==1
    text=text.replace(old,"    if grid==10:weights=[.004,.016,.064,.125,.25,.5,.75,1.]\n    elif grid==0:weights=[.001,.002,.003,.004,.006,.008,.012,.016]")
    compile(text,str(builder),'exec');assert not builder.exists();builder.write_text(text,encoding='utf8',newline='\n')
    controller=A/'run_continuous_fast_reused_frontiers_v11_20261010.py'
    text=(A/'run_continuous_fast_reused_frontiers_v10_20261010.py').read_text(encoding='utf8')
    text=text.replace('build_reused_neural_frontier_v7_20261010','build_reused_neural_frontier_v8_20261010').replace('continuous_fast_reused_frontiers_v10_20261010','continuous_fast_reused_frontiers_v11_20261010')
    start=text.index('            elif n<=168:');end=text.index('            if n==161 and not qualify_huber():break',start)
    text=text[:start]+"""            elif n<=172:
                # Prefer broad return/turnover-sensitive and structural coverage over tiny flagged adjustments.
                recipe,role=[('huber010','nonflag_valid'),('drop05','nonflag_valid'),('seed10','nonflag_valid'),
                    ('huber010','all_valid'),('seed09','all_valid'),('seed10','all_valid'),('drop05','all_valid'),
                    ('seed09','nonflag_valid'),('huber010','flag_valid'),('seed09','flag_valid'),
                    ('seed10','flag_valid'),('drop05','flag_valid')][n-161];grid=10
            else:
                expanded=list(itertools.product(('nonflag_valid','all_valid','flag_valid'),('huber010','seed09','seed10','drop05')))
                role,recipe=expanded[(n-173)%12];grid=1+(n-173)//12
"""+text[end:]
    text=text.replace("'weights':'two coarse grids, one wide/tiny grid, then deterministic bounded refinements fixed before each new score'",
                      "'weights':'high-impact broad grid .004 .016 .064 .125 .25 .5 .75 1 precedes refinements; train-only cumulative157 screen separately frozen'")
    text=text.replace("'role':'flag_valid','grid':0,'quality_cases':19,'QA':72", "'role':'nonflag_valid','grid':10,'quality_cases':19,'QA':72")
    compile(text,str(controller),'exec');assert not controller.exists();controller.write_text(text,encoding='utf8',newline='\n')
    # Concrete expressions are compiled, but no scores or proposed models are claimed qualified.
    namespace={'__file__':str(builder),'__name__':'high_impact_prospective_builder'}
    exec(compile(builder.read_text(encoding='utf8'),str(builder),'exec'),namespace)
    create(out/'prospective_source_controls.json',{'status':'passed_compile_and_grid_schedule_controls',
        'broad_weights':[.004,.016,.064,.125,.25,.5,.75,1.],'nonidentity_signed_cases':16,
        'first_new_bank_role':'nonflag_valid','fixed_complete_formal_base_round':152,
        'cumulative_screen_complete_parent_round':157,'scientific_math_codec_unchanged':True,
        'input_sha256':{str(p):sha(p) for p in (builder,controller,A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py')},
        'new_quality_scores':0})
    locations={'seed09':'actual_BF16Medium153_full5_independent_location_v1_20261009.json',
               'seed10':'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json',
               'drop05':'actual_BF16Drop05_156_full5_independent_location_v1_20261009.json'}
    cases=[{'recipe':None,'role':None,'sign':1.,'weight':0.}]
    for recipe in locations:
        for sign in (1.,-1.):
            for role in ('nonflag_valid','all_valid'):
                cases.extend({'recipe':recipe,'sign':sign,'role':role,'weight':w} for w in (.004,.016,.064,.125,.25,.5,.75,1.))
    assert len(cases)==97
    files=[A/'run_high_impact_cumulative_screen_v1_20261010.py',ROOT/'后续选模标准.md',ROOT/'evaluate.py',
        A/'BF16Medium153_complete_parent_rank_CDF_v1_20261009.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
        A/'score_calibrated_candidates_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',
        A/'all_forecast_percentile_runtime_20261007.py',A/'cached_official_spearman_runtime_20261007.py',
        A/'connected_validation_20261002/combined_fold_frame.parquet',
        *[A/'optimization_20261003_r157'/n for n in ('selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json')],
        A/'github_validation_sync_main_20261005/round157_receipt.json',
        *[ROOT/'candidates/optimization_20261003_r157'/n for n in ('verification.json','manifest.json')],
        *[A/'optimization_20261003_r95/scoring_validation_only'/n for n in ('测试集_X.csv','测试集_Y.csv')]]
    for name in locations.values():
        pointer=A/name;loc=read(pointer);folder=Path(loc['output'])
        assert sha(folder/'verification.json')==loc['verification_sha256']
        proof=read(folder/'verification.json');assert len(proof['records'])==5 and proof['rows_days_stocks']==[5635800,1212,4650]
        files.extend([pointer,folder/'verification.json',folder/'combined_raw.parquet'])
    plan=A/'high_impact_cumulative_screen_plan_v1_20261010.json'
    create(plan,{'status':'frozen97_training_only_cumulative_high_impact_candidates_before_scores','at_local':datetime.now().isoformat(),
        'parent_round':157,'cases':cases,'bank_locations':locations,'input_sha256':{str(p):sha(p) for p in files},
        'priority_reason':'Recent flag-only rounds158159 do not exceed157; broaden return/turnover-sensitive nonflag and all-stock mixtures after best complete157.',
        'official_connected_S_only':True,'test_labels_read':False,'future_X_read':False,'submission_qualified':False,
        'positive_screen_gain_requires_native_graph_freeze_reload_cold80_full_candidate_QA_main_before_adoption':True})
    # Stable py-spy wait boundaries exclude all dispatch and scientific worker activity.
    name='continuous_fast_reused_frontiers_v10_20261010';launch=read(A/'service_owned_workflows_20261006'/name/'native_launch.json')
    parent,worker,idle=suspended_idle(launch,'closed (run_continuous_fast_reused_frontiers_v10_20261010.py:')
    create(out/'old_controller_exact_idle.json',{'identity':launch,'stack':idle})
    retire_suspended(launch,'continuous_fast_reused_frontiers_v11_20261010')
    new=start_service('continuous_fast_reused_frontiers_v11_20261010',controller.name,[],{str(p):sha(p) for p in (controller,builder)})
    screen=start_service('actual_high_impact_cumulative_screen_v1_20261010','run_high_impact_cumulative_screen_v1_20261010.py',[],
                         {str(p):sha(p) for p in (plan,A/'run_high_impact_cumulative_screen_v1_20261010.py')})
    observer=A/'monitor_fast_optimization_v9_20261010.py'
    text=(A/'monitor_fast_optimization_v8_20261010.py').read_text(encoding='utf8')
    text=text.replace('continuous_fast_reused_frontiers_v10_20261010','continuous_fast_reused_frontiers_v11_20261010').replace('optimization_live_progress_v8_20261010','optimization_live_progress_v9_20261010')
    needle="        write(A/'optimization_live_progress_v9_20261010.json',state)"
    assert text.count(needle)==1
    text=text.replace(needle,"""        screen=Path('E:/赛题五_本机临时/high_impact_cumulative_screen_v1_20261010')
        screen_status={}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (screen/file).is_file():screen_status[key]=read(screen/file)
        screen_status['complete']=(screen/'verification.json').is_file()
        state['high_impact_cumulative_screen']=screen_status
"""+needle)
    text=text.replace("        target=A/'optimization_live_progress_v9_20261010.md'", "        text+=f\"\\n大幅度组合验证：{state['high_impact_cumulative_screen']}\\n\"\n        target=A/'optimization_live_progress_v9_20261010.md'")
    compile(text,str(observer),'exec');assert not observer.exists();observer.write_text(text,encoding='utf8',newline='\n')
    launch=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v8_20261010/native_launch.json')
    parent,worker,idle=suspended_idle(launch,'main (monitor_fast_optimization_v8_20261010.py:')
    create(out/'old_observer_exact_idle.json',{'identity':launch,'stack':idle})
    retire_suspended(launch,'actual_fast_optimization_progress_v9_20261010')
    progress=start_service('actual_fast_optimization_progress_v9_20261010',observer.name,[],{str(observer):sha(observer)})
    create(out/'verification.json',{'status':'passed_idle_only_priority_handoff_and_actual_hidden_cumulative_screen_launch',
        'controller':new,'screen':screen,'observer':progress,'existing_scientific_jobs_terminated':0,
        'score_changes_by_handoff':0,'test_labels_read':False,'submission_qualified':False,
        'first_broad_new_recipe':'Huber_delta0.1_rank_nonflag_valid','remaining_deadline':control['stop_at_local']})
    print({'controller':new['owned_worker_pid'],'screen':screen['owned_worker_pid'],'observer':progress['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
