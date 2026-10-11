"""Lightweight actual status snapshots for the resumed single-host pipeline."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys,time,os
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from scheduled_user_pause_20261007 import write

def main():
    import psutil
    alias=read(A/'manual_resume_service_aliases_v4_20261010.json')['service_aliases']
    while True:
        control=read(A/'current_user_runtime_control_20261010.json')
        current=datetime.now(timezone(timedelta(hours=8)))
        stages={}
        names={**alias,'main_publisher_v10_20261009':'main_publisher_v11_20261010',
               'BF16Drop05_156_complete_chronological_dispatch_v3_20261009':'BF16Drop05_156_complete_chronological_dispatch_manual_resume_v3_20261010'}
        names.update({n:n for n in [
          *['BF16Drop05_81_'+suffix+'_v1_20261009' for suffix in ('round156_source_admission','controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round156_full_registration')],
          'BF16FlagAfter15222_official_comparison_v3_20261009','BF16FlagAfter15222_round157_full_registration_v1_20261009']})
        loop=A/'continuous_fast_reused_frontiers_v19_20261010/state.json'
        if loop.is_file():
            loop_state=read(loop);current_round=loop_state.get('round')
            if current_round:
                count=loop_state.get('quality_cases',23 if current_round==158 else 19)
                prefix=f'ReusedNN{current_round}Quality{count}'
                current_jobs=[f'ReusedNN{current_round}Full17_actual_full_training_controls_v1_20261009',f'ReusedNN{current_round}Stage_actual_native14_calendar_v1_20261009',prefix+f'_round{current_round}_source_admission_v1_20261009',prefix+'_controls_main_publication_v1_20261009',prefix+'_official_comparison_v3_20261009',prefix+'_scores_main_publication_v1_20261009',prefix+'_selected_candidate_preparation_v1_20261009',prefix+'_selected_candidate_sealing_v1_20261009',prefix+f'_round{current_round}_full_registration_v1_20261009']
                names.update({k:k for k in current_jobs})
                if loop_state.get('actual_service'):names[loop_state['actual_service']]=loop_state['actual_service']
                if loop_state.get('full_service'):names[loop_state['full_service']]=loop_state['full_service']
        names.update({k:k for k in ['actual_BF16_medium2048_huber010_seed09_restart_control_v1_20261009','BF16Huber010161_independent_small_CPU_v1_20261009','actual_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009','BF16Huber010161_independent_full5_GPU_controls_v1_20261009','BF16Huber010161_actual_native42_calendar_v1_20261009']})
        names.update({k:k for k in ['continuous_fast_reused_frontiers_v19_20261010','HuberProtected163_complete67_family_v2_20261010','HuberProtected163_selected_native14_v1_20261010','HuberProtected163_selected_candidate_preparation_v1_20261010','HuberProtected163_selected_candidate_sealing_v1_20261010','HuberProtected163_round163_full_registration_v1_20261010','actual_causal_neural_smoothing73_screen_v1_20261010']})
        names.update({k:k for k in ['actual_BF16_medium2048_topweightedhuber010_seed09_restart_control_v1_20261009','BF16TopWeightedHuber010165_independent_small_CPU_v1_20261009','actual_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009','BF16TopWeightedHuber010165_independent_full5_GPU_controls_v1_20261009','BF16TopWeightedHuber010165_actual_native42_calendar_v1_20261009']})
        names.update({k:k for k in ['actual_TopWeighted_after163_high_impact65_screen_v1_20261010','actual_BF16_medium2048_returnhuber050_seed09_restart_control_v1_20261009','BF16ReturnHuber050166_independent_small_CPU_v1_20261009','actual_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009','BF16ReturnHuber050166_independent_full5_GPU_controls_v1_20261009','BF16ReturnHuber050166_actual_native42_calendar_v1_20261009']})
        names.update({k:k for k in ['actual_stock_identity_excess_prior_bank6_v3_20261010','actual_stock_identity_prior_after163_screen33_v3_20261010','actual_stock_identity_prior_bank_controls_main_v1_20261010','actual_stock_identity_prior_screen33_completion_main_v13_20261010']})
        for logical,name in names.items():
            visited=set()
            while name in alias and name not in visited:
                visited.add(name);name=alias[name]
            folder=A/'service_owned_workflows_20261006'/name
            row={'service':name,'status':'not_started'}
            if (folder/'native_launch.json').is_file():
                launch=read(folder/'native_launch.json')
                row.update(worker_pid=launch['owned_worker_pid'],status='running' if owned(launch) else 'stopped_or_finished')
                if (folder/'service_execution.json').is_file():row['execution']=read(folder/'service_execution.json');row['status']=row['execution']['status']
                log=folder/'stdout.log'
                if log.is_file():
                    with log.open('rb') as stream:
                        stream.seek(max(0,log.stat().st_size-2200));row['recent_log']=stream.read().decode('utf8',errors='replace')[-1300:]
            stages[logical]=row
        bank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009')
        state={'status':'actual_optimization_running_until_explicit_deadline',
               'at_local':current.isoformat(),'deadline_local':control['stop_at_local'],
               'best_fully_qualified':read(A/'latest_verified_submission_delivery_v2_20261008.json'),
               'completed_drop05_annual_models':[y for y in range(2020,2026) if (bank/str(y)/'info.json').is_file()],
               'annual_training_stage':read(bank/'actual_stage.json'),'jobs':stages,
               'available_memory_GiB':psutil.virtual_memory().available/2**30,
               'disk_free_GiB':{d:psutil.disk_usage(d+':/').free/2**30 for d in ('D','E')},
               'new_scores_by_observer':0,'test_labels_read':False,
               'recovery_manifest':str(A/'failed_dependency_and_cold80_recovery_v2_20261010/verification.json'),
               'fully_qualified_rounds':[n for n in range(152,1001) if (A/f'optimization_20261003_r{n}/full_registration_execution.json').is_file()]}
        for number,family in ((156,'BF16Drop05_81'),(157,'BF16FlagAfter15222')):
            folder=A/(family+'_official_comparison_v1_20261009')
            state['round'+str(number)]={'actual_saved_score_records':len(list(folder.glob('case*_official.json'))),
                                     'complete':(folder/'verification.json').is_file()}
            if state['round'+str(number)]['complete']:state['round'+str(number)]['best']=read(folder/'verification.json')['best']
        loop=A/'continuous_fast_reused_frontiers_v19_20261010/state.json'
        if loop.is_file():
            state['continuous_reused_frontiers']=read(loop)
            number=state['continuous_reused_frontiers'].get('round')
            if number:
                count=state['continuous_reused_frontiers'].get('quality_cases',23 if number==158 else 19)
                quality=A/f'ReusedNN{number}Quality{count}_official_comparison_v1_20261009'
                state['continuous_reused_frontiers']['actual_saved_official_scores']=len(list(quality.glob('case*_official.json')))
                state['continuous_reused_frontiers']['official_score_complete']=(quality/'verification.json').is_file()
                if number in (162,163):
                    pilot=Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/pilot76.json' if number==162 else 'E:/赛题五_本机临时/protected_Huber_selected_native14_v1_20261010/pilot67.json')
                    state['continuous_reused_frontiers']['actual_saved_official_scores']=len(read(pilot)['records']) if pilot.is_file() else 0
                    state['continuous_reused_frontiers']['official_score_complete']=pilot.is_file()
                    state['continuous_reused_frontiers']['registered_reused_scores_not_new_evaluations']=True
        screen=Path('E:/赛题五_本机临时/high_impact_cumulative_screen_v2_20261010')
        screen_status={}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (screen/file).is_file():screen_status[key]=read(screen/file)
        screen_status['complete']=(screen/'verification.json').is_file()
        state['high_impact_cumulative_screen']=screen_status
        protected=Path('E:/赛题五_本机临时/protected_upper_tail_screen_v1_20261010')
        protected_status={}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (protected/file).is_file():protected_status[key]=read(protected/file)
        protected_status['complete']=(protected/'verification.json').is_file()
        state['protected_upper_tail_screen']=protected_status
        exact_top=Path('E:/赛题五_本机临时/protected_official_top_screen_v2_20261010')
        exact_status={}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (exact_top/file).is_file():exact_status[key]=read(exact_top/file)
        exact_status['complete']=(exact_top/'verification.json').is_file()
        state['protected_official_top_screen']=exact_status
        huber=Path('E:/赛题五_本机临时/neural_BF16_medium2048_huber010_seed09_e64_bank6_v1_20261009')
        state['actual_Huber_annual_training']={'completed_annual_models':[y for y in range(2020,2026) if (huber/str(y)/'info.json').is_file()]}
        if (huber/'actual_stage.json').is_file():state['actual_Huber_annual_training']['stage']=read(huber/'actual_stage.json')
        new_screen=Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010')
        state['new_Huber65_screen']={'expected_cases':65,'complete':(new_screen/'verification.json').is_file(),'queued_after_own_Huber6_full5_native42':True}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (new_screen/file).is_file():state['new_Huber65_screen'][key]=read(new_screen/file)
        state['protected162_full_chain_descriptor_installed']=(A/'TailProtected162_full76_ready_dispatch_v1_20261010.json').is_file()
        compression=Path('E:/赛题五_本机临时/protected_quantization37_screen_v1_20261010')
        state['no_fit_quantization37_screen']={'expected_cases':37,'complete':(compression/'verification.json').is_file(),'new_native_fits':0}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (compression/file).is_file():state['no_fit_quantization37_screen'][key]=read(compression/file)
        budgeted=Path('E:/赛题五_本机临时/budgeted_neural_Top37_screen_v1_20261010')
        state['budgeted_neural_Top37_screen']={'expected_cases':37,'complete':(budgeted/'verification.json').is_file(),'new_native_fits':0}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (budgeted/file).is_file():state['budgeted_neural_Top37_screen'][key]=read(budgeted/file)
        state['actual_Huber_annual_training']['actual_training_bank_completed']=(huber/'verification.json').is_file() and read(huber/'verification.json').get('actual_native_fits')==6
        temporal=Path('E:/赛题五_本机临时/causal_neural_smoothing73_screen_v1_20261010')
        state['causal_neural_smoothing73_screen']={'expected_cases':73,'complete':(temporal/'verification.json').is_file(),'new_native_fits':0}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (temporal/file).is_file():state['causal_neural_smoothing73_screen'][key]=read(temporal/file)
        topbank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_topweightedhuber010_seed09_e64_bank6_v1_20261009')
        state['actual_new_TopWeighted_training']={'completed_annual_models':[y for y in range(2020,2026) if (topbank/str(y)/'info.json').is_file()],'six_fit_verification_complete':(topbank/'verification.json').is_file(),'quality_scores_not_claimed_until_own_full5_and_native42':True}
        if (topbank/'actual_stage.json').is_file():state['actual_new_TopWeighted_training']['stage']=read(topbank/'actual_stage.json')
        returnbank=Path('E:/赛题五_本机临时/neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009')
        state['actual_new_ReturnHuber_training']={'completed_annual_models':[y for y in range(2020,2026) if (returnbank/str(y)/'info.json').is_file()],'six_fit_verification_complete':(returnbank/'verification.json').is_file(),'quality_scores_not_claimed_until_own_full5_and_native42':True}
        if (returnbank/'actual_stage.json').is_file():state['actual_new_ReturnHuber_training']['stage']=read(returnbank/'actual_stage.json')
        topscreen=Path('E:/赛题五_本机临时/TopWeighted_after163_high_impact65_screen_v1_20261010')
        state['TopWeighted_after163_screen']={'complete':(topscreen/'verification.json').is_file(),'expected_cases':65}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (topscreen/file).is_file():state['TopWeighted_after163_screen'][key]=read(topscreen/file)
        stockbank=Path('E:/赛题五_本机临时/stock_identity_excess_prior_bank6_v3_20261010')
        state['actual_stock_identity_prior_training']={'completed_annual_models':[y for y in range(2020,2026) if (stockbank/str(y)/'info.json').is_file()],'six_fit_verification_complete':(stockbank/'verification.json').is_file(),'original_precision_and_reporting_failures_retained':True,'quality_scores_not_claimed_by_training':True}
        stockscreen=Path('E:/赛题五_本机临时/stock_identity_prior_after163_screen33_v3_20261010')
        state['stock_identity_prior_screen33']={'expected_cases':33,'complete':(stockscreen/'verification.json').is_file()}
        for key,file in [('stage','actual_stage.json'),('best_so_far','best_so_far.json')]:
            if (stockscreen/file).is_file():state['stock_identity_prior_screen33'][key]=read(stockscreen/file)
        screen_rows=[]
        for family in ('high_impact_cumulative_screen_v2_20261010','protected_upper_tail_screen_v1_20261010','protected_official_top_screen_v2_20261010','Huber010_high_impact65_screen_v1_20261010','protected_quantization37_screen_v1_20261010','budgeted_neural_Top37_screen_v1_20261010','causal_neural_smoothing73_screen_v1_20261010','TopWeighted_after163_high_impact65_screen_v1_20261010','stock_identity_prior_after163_screen33_v3_20261010'):
            for record_path in (Path('E:/赛题五_本机临时')/family).glob('case*_official.json'):
                row=read(record_path)
                screen_rows.append({'family':family,'case':row['case'],'configuration':row['configuration'],
                    'S':row['connected_final_score'],'gain':row['score_gain_over_qualified_parent'],
                    'IC':row['metrics']['ic_mean'],'annual_excess':row['metrics']['annual_excess'],
                    'turnover':row['metrics']['mean_turnover'],'source':str(record_path),'submission_qualified':False})
        screen_rows.sort(key=lambda r:(-r['S'],r['family'],r['case']))
        state['new_high_impact_verified_score_records']=len(screen_rows)
        write(A/'high_impact_additional_validation_rankings_v1_20261010.json',{'at_local':current.isoformat(),
            'status':'actual_completed_training_only_official_scores_new_scheme_qualification_pending','records':screen_rows,
            'current_fully_qualified_delivery':state['best_fully_qualified'],'test_labels_read':False})
        write(A/'optimization_live_progress_v20_20261010.json',state)
        text=f"更新时间：{state['at_local']}\n\n优化截止：{state['deadline_local']}\n\n当前最佳合格方案：第{state['best_fully_qualified']['selected_round']}轮，官方S={state['best_fully_qualified']['official_score']:.15f}\n\n第156轮年度模型：{len(state['completed_drop05_annual_models'])}/6；官方分数：{state['round156']['actual_saved_score_records']}/81\n\n第157轮官方分数：{state['round157']['actual_saved_score_records']}/22\n\n各任务状态以同名JSON为准；新Top与直接收益率训练进度见下方。\n"
        if 'continuous_reused_frontiers' in state:text+=f"\n连续扩展：{state['continuous_reused_frontiers']}\n"
        text+=f"\n大幅度组合验证：{state['high_impact_cumulative_screen']}\n"
        text+=f"\n保留高分股票的组合验证：{state['protected_upper_tail_screen']}\n"
        text+=f"\n严格保留Top的组合验证：{state['protected_official_top_screen']}\n\n新Huber年度训练：{state['actual_Huber_annual_training']}\n"
        text+=f"\n新Huber完整157之后65项组合验证：{state['new_Huber65_screen']}\n"
        text+=f"\n无需新拟合的低分区压缩37项验证：{state['no_fit_quantization37_screen']}\n"
        text+=f"\n每日主动换股预算37项验证：{state['budgeted_neural_Top37_screen']}\n"
        text+=f"\n新Top加权训练：{state['actual_new_TopWeighted_training']}\n\n当前最佳163之后65项组合：{state['TopWeighted_after163_screen']}\n\n新直接收益率训练：{state['actual_new_ReturnHuber_training']}\n"
        text+=f"\n股票历史超额收益先验拟合：{state['actual_stock_identity_prior_training']}\n\n先验33项组合：{state['stock_identity_prior_screen33']}\n"
        target=A/'optimization_live_progress_v20_20261010.md';temporary=target.with_suffix('.tmp')
        temporary.write_text(text,encoding='utf8');os.replace(temporary,target)
        if current>=datetime.fromisoformat(control['stop_at_local']) or control['status']!='optimization_active_after_explicit_manual_resume':break
        time.sleep(20)

if __name__=='__main__':main()
