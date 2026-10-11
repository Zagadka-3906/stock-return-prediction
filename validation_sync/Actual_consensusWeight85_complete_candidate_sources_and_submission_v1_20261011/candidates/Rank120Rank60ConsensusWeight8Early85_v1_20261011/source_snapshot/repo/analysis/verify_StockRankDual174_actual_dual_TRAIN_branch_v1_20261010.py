"""Execute real candidate dual branch over actual three-day TRAIN fixtures for all24 cases."""
from pathlib import Path
import sys,os,ast,hashlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/stock_rank_dual174_actual_dual_TRAIN_branch_v1_20261010')
for key in ('TMP','TEMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp'/key)
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_stock_rank_embedding_own_training_queue_v2_20261010')
    import numpy as np,polars as pl,importlib
    import dual_target_daily_rank_consensus_v1_20261010 as dual
    source=A/'prepare_StockRankDual174_selected_candidate_v1_20261010.py';tree=ast.parse(source.read_text(encoding='utf8'))
    branches=[n for n in ast.walk(tree) if isinstance(n,ast.If) and ast.unparse(n.test)=='len(leaves) == 2']
    assignments=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='selected' for t in n.targets)]
    assert len(branches)==len(assignments)==1
    code=compile(ast.fix_missing_locations(ast.Module(body=[branches[0],assignments[0]],type_ignores=[])),str(source)+'::actual_dual_TRAIN_branch','exec')
    from run_stock_dual_embedding_after173_high_impact25_screen_v1_20261010 import cases
    plan=cases();assert len(plan)==25
    paths=[source,Path(__file__),A/'stock_dual_embedding_after173_predeclared25_plan_v1_20261010.json',Path(dual.__file__),A/'stock_rank_dual174_candidate_sources_preparation_v1_20261010.json']
    folders=[Path(read(A/pointer)['output']) for pointer in ('actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json','actual_StockRankEmbeddingSmall512_full5_independent_location_v1_20261009.json')]
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r170/selected_validation.npy'
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']).head(13950)
    signals=[pl.read_parquet(folder/'combined_raw.parquet').head(13950) for folder in folders]
    for signal in signals:assert signal.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
    OUT.mkdir(exist_ok=True);assert not (OUT/'frozen_before24.json').exists()
    second_path=OUT/'actual_rank_three_day_TRAIN.parquet';assert not second_path.exists();signals[1].write_parquet(second_path)
    paths += [framepath,parentpath,second_path,*[folder/'verification.json' for folder in folders],*[folder/'combined_raw.parquet' for folder in folders]]
    pins={str(p):sha(p) for p in paths};create(OUT/'frozen_before24.json',{'input_sha256':pins,'expected_cases':24,'all_arrays_TRAIN_only':True,'reference_parent_round':170,'quality_parent173_not_yet_complete':True})
    raw=np.load(parentpath,mmap_mode='r')[:13950];return_raw=signals[0]['pred_raw'].to_numpy();rank_raw=signals[1]['pred_raw'].to_numpy();dates,flags,valid=[frame[c].to_numpy() for c in ('trade_date','flag_limit_up','price_valid')];records=[]
    codecs={'valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010','official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}
    for c in plan[1:]:
        assert allowed();cfg={**c,'codec':c['kind'],'decay':None,'stage_kind':'stock_return_rank_embedding_consensus'};module=importlib.import_module(codecs[cfg['codec']])
        scope={'cfg':cfg,'leaves':[{},{}],'pl':pl,'frame':frame,'neural_paths':[None,second_path],'neural':return_raw.copy(),'raw':raw,'dates':dates,'flags':flags,'valid':valid,'transform':module.transform};exec(code,scope)
        expected_mix=dual.pandas_oracle(return_raw,rank_raw,dates,cfg['mean_weight'])
        assert np.array_equal(scope['neural'].view('u8'),expected_mix.view('u8'))
        oracle=module.pandas_oracle(raw,expected_mix,dates,flags,valid,cfg['weight'],cfg['protect_fraction'],cfg['sign'])
        value=scope['selected'];assert np.array_equal(value.view('u8'),oracle.view('u8'))
        module.assert_invariants(raw,value,dates,flags,valid,cfg['protect_fraction'])
        row={'configuration':cfg,'rows':13950,'actual_candidate_dual_branch_and_independent_Pandas_bits_exact':True,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()};create(OUT/f'case{len(records):02d}.json',row);records.append(row)
    assert len(records)==24
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_actual24_candidate_dual_TRAIN_branches_13950_rows_independent_Pandas_and_invariants','input_sha256':pins,'records':records,'new_quality_scores':0,'actual_full5635800_dual_selected_reconstruction_not_claimed':True,'actual_future_X_read':False,'test_labels_read':False})
    create(A/'actual_stock_rank_dual174_dual_TRAIN_branch_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_candidate_dual_branches_passed':24,'rows_each':13950,'future_X_read':False},flush=True)
if __name__=='__main__':main()
