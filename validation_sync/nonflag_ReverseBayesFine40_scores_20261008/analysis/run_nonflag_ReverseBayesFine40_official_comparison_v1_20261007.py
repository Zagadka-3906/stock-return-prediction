"""Score88 predeclared refinements, retaining complete compatible parents and all qualified anchors."""
from pathlib import Path
from types import SimpleNamespace
import gc
import hashlib
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write
OUT=A/'nonflag_ReverseBayesFine40_official_comparison_v1_20261007'


def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    assert read(f/'service_execution.json')['status']=='passed',name


def main():
    import numpy as np
    import polars as pl
    import psutil
    from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared,transform
    from nonflag_residual_ReverseBayesFine_compatible_parent_20261007 import compatible
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as installed_percentile
    from cached_official_spearman_runtime_20261007 import installed as installed_ic
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    assert not OUT.exists();OUT.mkdir()
    for name in ('nonflag_ReverseBayesFine40_actual_full37_controls_v1_20261008','CPU_HGB44_round112_full_registration_v2',
        'nonflag_ReverseBayes40_round132_full_registration_v1','nonflag_SparseGram40_round133_full_registration_v1'):
        closed(name)
    for number,version in ((112,23),(132,43),(133,44)):
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['actual_full_QA_version']==version
    gate=A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json'
    assert read(gate)['status']=='passed_actual4_uncached_full_official_calls_at_8_5GiB_start_gate_all8_and_CSV_and_input_bits_exact'
    while psutil.virtual_memory().available<8.5*2**30:time.sleep(15)
    plan_path=A/'nonflag_ReverseBayesFine40_plan_20261007.json';plan=read(plan_path)
    preflight=A/'nonflag_residual_ReverseBayesFine37_transform_preflight_20261007/verification.json'
    assert read(preflight)['status']=='passed_actual37_full5635800_nonflag_ReverseBayes64_independent_CDF_and111_cold_controls'
    bank=A/plan['existing_native_bank'];bank_proof=read(bank/'verification.json')
    assert bank_proof['actual_native_fits']==len(bank_proof['actual_models'])==10
    reference_candidate=ROOT/'candidates/simplex_residual47_20261006'
    reference_graph=read(reference_candidate/'verification.json')['whole_scheme_graph']
    parents={n:A/f'optimization_20261003_r{n}' for n in plan['qualified_anchor_rounds']}
    baselines={n:read(p/'calibrated_csv_official.json')['metrics'] for n,p in parents.items()}
    graphs={n:read(ROOT/f'candidates/optimization_20261003_r{n}/verification.json')['whole_scheme_graph'] for n in parents}
    eligible=[n for n in parents if compatible(graphs[n],reference_graph) and 'protected_upper_pool_CPU_HGB_CDF' not in graphs[n]];assert 112 in eligible
    comparison_parent=min(parents,key=lambda n:(-baselines[n]['final_score'],n))
    scheme_base=min(eligible,key=lambda n:(-baselines[n]['final_score'],n))
    components={name:[name] for name in plan['single_native_heads']};components.update(plan['ensembles']);components['remove_nonflag_ReverseBayes64']=[]
    cases=[{'anchor_round':n,'model':None,'weight':0.,'universe':None} for n in parents]
    cases += [{'anchor_round':scheme_base,'model':name,'weight':weight,'universe':plan['universe']}
        for name in [*plan['single_native_heads'],*plan['ensembles']] for weight in plan['weights']]
    cases += [{'anchor_round':scheme_base,'model':'remove_nonflag_ReverseBayes64','weight':0.,'universe':plan['universe']}]
    assert plan['residual_sign']==-1
    for case in cases:
        if case['model'] is not None:case['residual_sign']=-1
    assert len(cases)==plan['expected_scored_records']==40
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    reference_path=A/'optimization_20261003_r106/selected_validation.npy'
    sources=[Path(__file__),plan_path,preflight,A/'nonflag_residual_HGB_CDF_transform_20261007.py',A/'nonflag_residual_ReverseBayesFine_compatible_parent_20261007.py',
        A/'conditional_residual_mlp_CDF_transform_20261007.py',A/'direct_flag_centered_rank_CDF_transform_20261007.py',
        A/'score_calibrated_candidates_20261003.py',A/'official_date_index_dataframe_adapter_20261007.py',
        A/'all_forecast_percentile_runtime_20261007.py',A/'cached_official_spearman_runtime_20261007.py',
        A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',
        A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json',ROOT/'evaluate.py',ROOT/'后续选模标准.md',frame_path,reference_path,reference_candidate/'verification.json',bank/'verification.json']
    sources += list(bank.glob('*/nonflag_oof_predictions.npy'))+list(bank.glob('*/info_*.json'))+list(bank.glob('*/model_*.joblib'))+list(bank.glob('*/independent_linear_state_*.json'))
    for n,p in parents.items():
        sources += [p/name for name in ('selection.json','protocol.json','selected_validation.npy','calibrated_csv_official.json','full_registration_execution.json')]
        candidate=ROOT/f'candidates/optimization_20261003_r{n}'
        sources += [candidate/'verification.json',candidate/'manifest.json',A/f'github_validation_sync_main_20261005/round{n}_receipt.json']
    scoring_source=A/'optimization_20261003_r95/scoring_validation_only';sources += [scoring_source/n for n in ('测试集_X.csv','测试集_Y.csv')]
    pins={**bank_proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(OUT/'frozen_before_actual_full_controls_and_official_scores.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'cases':cases,'components':components,'actual_comparison_parent_round':comparison_parent,
        'actual_scheme_base_round':scheme_base,'baseline_metrics':baselines,'structurally_compatible_parent_rounds':eligible,
        'incompatible_anchors_retained_as_candidates':True,'reference106_core_and_feature_teacher_unchanged':True,
        'all_forecast_transform_inputs_current_X_or_reference_forecasts_no_Y':True,'new_native_fits':0,
        'selection_bias_uncorrected':True,'no_extra_Top_worst_year_or_significance_gate':True,'test_labels_read':False})
    records=[];target_rank_cache={}
    with LockedReadHashCache(pins) as scope:
        frame=pl.read_parquet(frame_path,columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        reference=np.load(reference_path,mmap_mode='r');parent=np.load(parents[scheme_base]/'selected_validation.npy',mmap_mode='r')
        head={n:np.load(bank/n/'nonflag_oof_predictions.npy',mmap_mode='r') for n in plan['single_native_heads']}
        for name,names in plan['ensembles'].items():
            values=np.zeros(len(reference),dtype=np.float64)
            for n in names:values+=head[n]
            values/=len(names);head[name]=values
        head['remove_nonflag_ReverseBayes64']=np.zeros(len(reference),dtype=np.float64)
        head={name:-np.asarray(values) for name,values in head.items()}
        prepared=prepare(reference,dates,flags,valid,plan['universe']);days,starts=np.unique(dates,return_index=True);ends=np.r_[starts[1:],len(dates)]
        scoring=OUT/'scoring_validation_only';scoring.mkdir()
        for n in ('测试集_X.csv','测试集_Y.csv'):os.link(scoring_source/n,scoring/n)
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);preserved=flags==1
        for index,cfg in enumerate(cases):
            if cfg['model'] is None:values=np.asarray(np.load(parents[cfg['anchor_round']]/'selected_validation.npy',mmap_mode='r'))
            else:
                values=apply_prepared(parent,reference,flags,head[cfg['model']],cfg['weight'],prepared)
                assert np.array_equal(values[preserved].view('u8'),parent[preserved].view('u8'))
                assert np.array_equal(values[dates<20210101].view('u8'),parent[dates<20210101].view('u8'))
                for count in (80,260,975):
                    n=int(ends[count-1]);cold=transform(parent[:n],reference[:n],dates[:n],flags[:n],valid[:n],head[cfg['model']][:n],cfg['weight'],plan['universe'])
                    assert np.array_equal(values[:n].view('u8'),cold.view('u8'))
            write(OUT/'actual_stage.json',{'status':'actual_full_official_scoring','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                'case':index,'configuration':cfg,'actual_completed_cases':len(records),'expected_cases':40})
            with installed_percentile() as percentile_runtime, installed_ic(target_rank_cache) as ic_runtime:
                with installed(scoring/'submission.csv') as date_index:metrics=score(ctx,values)
            if cfg['model'] is None:assert metrics==baselines[cfg['anchor_round']]
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            item={'case':index,'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],
                'score_gain_over_qualified_parent':metrics['final_score']-baselines[comparison_parent]['final_score'],
                'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':scheme_base,
                'prediction_numeric_bytes_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest(),
                'official_date_index_runtime':dict(date_index),'all_row_percentile_runtime':percentile_runtime,'scoring_only_spearman_runtime':ic_runtime,'official_score_cache':ctx.last_official_score_cache,
                'official_metric_capsule_sha256':sha(capsule),'actual_return_mapping':ctx.last_candidate_return_mapping,
                'all_complete_parent_flag_and2020_raw_bits_preserved':cfg['model'] is not None,
                'actual_cold80_260_975_bits_exact':cfg['model'] is not None,'qualified_anchor_all8_metrics_exact':cfg['model'] is None,
                'native_bank_source':str(bank/'verification.json'),'ordered_native_components':components.get(cfg['model']),
                'reference106_feature_teacher_unchanged':True,'official_Top_invariance_not_used_as_selection_gate':True,
                'candidate_full_future_freeze_native_replays_QA45_and_main_pending':True,'test_labels_read':False}
            create(OUT/f'case{index:02d}_official.json',item);records.append(item)
            print({'case':index,'score':metrics['final_score'],'gain':item['score_gain_over_qualified_parent']},flush=True)
            del values;gc.collect()
        scope.reverify()
    best=min(records,key=lambda r:(-r['connected_final_score'],r['configuration']['weight'],r['case']))
    create(OUT/'verification.json',{'status':'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'best':best,'components':components,
        'actual_comparison_parent_round':comparison_parent,'actual_scheme_base_round':scheme_base,
        'existing_native_bank_fits':10,'new_native_fits_by_comparison':0,'new_quality_score_records':40,
        'all37_nonanchors_full_and_cold_controls_passed':True,'future_candidate_and_full134_qualification_pending':True,
        'global_feasible_direction_or_resource_exhaustion_not_established':True,'test_labels_read':False})


if __name__=='__main__':main()
