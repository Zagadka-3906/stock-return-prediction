"""Test causal parent-only bounded optional Top changes on the complete connected TRAIN panel."""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import sys,os,time,json,hashlib,gc,shutil
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A),str(A/'connected_validation_20261002')]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
OUT=Path('E:/赛题五_本机临时/parent169_causal_Top_stability19_screen_v1_20261010')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def write(path,value):
    temporary=path.with_name(path.name+f'.{os.getpid()}.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8');os.replace(temporary,path)

def cases():
    result=[{'recipe':None,'weight':0.,'budget_fraction':None,'margin':None,'sign':1.}]
    for budget in (0.,.002,.005,.01,.02,.04):
        for margin in (0.,.005,.02):
            result.append({'recipe':'whole169_parent_only','weight':1.,'budget_fraction':budget,'margin':margin,'sign':1.})
    assert len(result)==19;return result

def main():
    assert allowed();closed('FastNeuralFrontier169_round169_full_registration_external_capsule_resume_v3_20261010')
    import numpy as np,polars as pl,psutil
    import budgeted_neural_Top_projection_v1_20261010 as codec
    from score_calibrated_candidates_20261003 import score
    from official_date_index_dataframe_adapter_20261007 import installed
    from all_forecast_percentile_runtime_20261007 import installed as percentiles
    from cached_official_spearman_runtime_20261007 import installed as spearman
    from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed as exact_E_guard
    control_path=A/'budgeted_neural_Top_projection_controls_v1_20261010.json'
    proof=read(control_path);assert proof['status'].startswith('passed48_')
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest
    sources=[Path(__file__),Path(codec.__file__),control_path,ROOT/'后续选模标准.md',
        A/'optimization_20261003_r169/selected_validation.npy',A/'optimization_20261003_r169/calibrated_csv_official.json',
        A/'connected_validation_20261002/combined_fold_frame.parquet',A/'github_validation_sync_main_20261005/round169_receipt.json',
        A/'exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py',A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json']
    pins={str(p):sha(p) for p in sources};plan=cases();OUT.mkdir(exist_ok=False)
    create(OUT/'frozen_before_any_new_controls_or_scores.json',{'status':'frozen19_parent169_only_causal_Top_optional_budget_hypotheses','input_sha256':pins,'cases':plan,
        'parent_round':169,'stock_identity':'verified_fixed_sorted_stock_row_positions','empty_first_day_state_original_parent_Top':True,
        'continuous2020_to2024_state_no_annual_reset':True,'actual_official_turnover_not_assumed_equal_to_optional_swap_budget':True,
        'new_native_fits':0,'future_X_read':False,'test_labels_read':False})
    scoring=OUT/'scoring_validation_only';scoring.mkdir()
    for name in ('测试集_X.csv','测试集_Y.csv'):
        original=A/'optimization_20261003_r95/scoring_validation_only'/name
        shutil.copyfile(original,scoring/name);assert sha(original)==sha(scoring/name)
    scratch=OUT/'tmp';scratch.mkdir()
    for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(scratch)
    import tempfile;tempfile.tempdir=str(scratch)
    with exact_E_guard(scoring,OUT/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):
        while psutil.virtual_memory().available<11.5*2**30:assert allowed();time.sleep(15)
        frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid','y_ret_1d'])
        assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
        codes=frame['ts_code'].to_numpy().reshape(1212,4650);assert np.all(codes==codes[0]) and len(set(codes[0]))==4650
        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]
        parent=np.load(A/'optimization_20261003_r169/selected_validation.npy',mmap_mode='r')
        baseline=read(A/'optimization_20261003_r169/calibrated_csv_official.json')['metrics']
        ctx=SimpleNamespace(frame=frame,dates=dates,scoring=scoring);rank_cache={};records=[]
        prepared=codec.ranks.prepare(parent,np.asarray(parent),dates,flags,valid,1.)
        exact=lambda a,b:np.array_equal(np.asarray(a,dtype=np.float64).view('u8'),np.asarray(b,dtype=np.float64).view('u8'))
        for index,configuration in enumerate(plan):
            assert allowed();prefix_controls=[];started=time.perf_counter()
            if not index:value=np.asarray(parent);trace=[]
            else:
                arguments=(configuration['weight'],configuration['budget_fraction'],configuration['margin'])
                value,trace=codec.apply_prepared(parent,flags,valid,*arguments,prepared,return_trace=True)
                oracle,oracle_trace=codec.pandas_oracle(parent,np.asarray(parent),dates,flags,valid,*arguments,1.,return_trace=True)
                assert exact(value,oracle) and trace==oracle_trace;del oracle,oracle_trace
                unselected=~((flags==0)&valid);assert exact(value[unselected],parent[unselected]) and exact(value[:4650],parent[:4650])
                assert all(row['optional_swaps']<=row['budget'] for row in trace)
                for days in (80,260,975):
                    n=days*4650
                    prefix=codec.transform(parent[:n],np.asarray(parent[:n]),dates[:n],flags[:n],valid[:n],*arguments,1.)
                    oracle=codec.pandas_oracle(parent[:n],np.asarray(parent[:n]),dates[:n],flags[:n],valid[:n],*arguments,1.)
                    assert exact(value[:n],prefix) and exact(prefix,oracle)
                    prefix_controls.append({'days':days,'native_and_independent_Pandas_bits_exact':True});del prefix,oracle
            numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()
            control={'case':index,'configuration':configuration,'rows':len(value),'full_independent_Pandas_exact':bool(index),
                'prefix_controls':prefix_controls,'numeric_sha256':numeric,'optional_budget_trace':trace,
                'stock_identity_grid_verified':True,'state_not_reset_at_annual_boundaries':True,'future_X_read':False}
            create(OUT/f'case{index:03d}_controls.json',control)
            write(OUT/'actual_stage.json',{'case':index,'completed_cases':len(records),'expected_cases':19,'at_local':datetime.now().isoformat()})
            assert allowed()
            with percentiles(),spearman(rank_cache),installed(scoring/'submission.csv'):metrics=score(ctx,value)
            if not index:assert metrics==baseline
            capsule=Path(ctx.last_official_score_cache['official_metrics_source'])
            row={'case':index,'configuration':configuration,'metrics':metrics,'connected_final_score':metrics['final_score'],
                'score_gain_over_qualified_parent':metrics['final_score']-baseline['final_score'],'control_sha256':sha(OUT/f'case{index:03d}_controls.json'),
                'prediction_numeric_sha256':numeric,'official_metric_capsule_sha256':sha(capsule),'official_score_cache':ctx.last_official_score_cache,
                'actual_return_mapping':ctx.last_candidate_return_mapping,'new_native_fits':0,'submission_qualified':False,
                'future_X_read':False,'test_labels_read':False,'selection_bias_uncorrected':True}
            create(OUT/f'case{index:03d}_official.json',row);records.append(row)
            write(OUT/'best_so_far.json',{'completed_cases':len(records),'expected_cases':19,'best':max(records,key=lambda r:r['connected_final_score']),'submission_qualified':False})
            print({'case':index,'configuration':configuration,'S':metrics['final_score'],'gain':row['score_gain_over_qualified_parent'],'seconds':time.perf_counter()-started},flush=True)
            del value;gc.collect()
        for path,digest in pins.items():assert sha(path)==digest
        create(OUT/'verification.json',{'status':'passed19_parent169_only_causal_bounded_Top_actual_training_only_official_comparisons',
            'input_sha256':pins,'records':records,'best':max(records,key=lambda r:r['connected_final_score']),
            'new_quality_score_records':19,'actual_nonidentity_full_controls':18,'actual_nonidentity_prefix_controls':54,
            'new_native_fits':0,'submission_qualified':False,'future_X_read':False,'test_labels_read':False})
        create(A/'actual_parent169_causal_Top_stability19_screen_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})

if __name__=='__main__':main()
