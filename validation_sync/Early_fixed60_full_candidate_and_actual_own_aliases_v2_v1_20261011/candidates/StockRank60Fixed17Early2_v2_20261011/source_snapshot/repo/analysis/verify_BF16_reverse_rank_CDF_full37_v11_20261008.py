"""Full37 independent transforms and111 cold prefixes after real6 fits and actual134 closure."""
from pathlib import Path
import gc
import os
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/BF16_reverse_rank_CDF_full37_preflight_v1_20261008')
for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR'):os.environ[key] = str(OUT / 'tmp' / key)
from run_dependency_queue_v3_20261006 import read, sha, create, owned


def closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status'] == 'passed', name


def main():
    closed('BF16_independent_full5_GPU_controls_v2_20261008')
    closed('Huber52_round137_full_registration_v11_20261008')
    import numpy as np
    import polars as pl
    import psutil
    import BF16_reverse_complete_parent_rank_CDF_v1_20261008 as codec
    plan_path = A / 'BF16reverse40_round138_plan_v1_20261008.json'
    plan = read(plan_path)
    assert plan['expected_scored_records'] == 40 and len(plan['weights']) == 12 and len(plan['roles']) == 3
    assert plan['first2020_active'] and plan['rank_universe'] == 'all_current_raw_forecasts'
    neural_folder = Path(read(A/'actual_BF16_full5_independent_location_v2_20261008.json')['output'])
    neural_proof = read(neural_folder/'verification.json')
    assert neural_proof['status'] == 'passed_actual_full5_5635800_BF16_native_and_independent_GPU_forecasts_and10_cold_prefixes'
    parents = plan['qualified_anchor_rounds']
    metrics = {}
    for number in parents:
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status'] == 'passed'
        assert read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json')['status'] == 'pushed_and_remote_head_verified'
        metrics[number] = read(A/f'optimization_20261003_r{number}/calibrated_csv_official.json')['metrics']
    parent = min(parents, key=lambda number: (-metrics[number]['final_score'],len(read(ROOT/f'candidates/optimization_20261003_r{number}/verification.json')['models']),number))
    frame_path = A/'connected_validation_20261002/combined_fold_frame.parquet'
    parent_path = A/f'optimization_20261003_r{parent}/selected_validation.npy'
    neural_path = neural_folder/'combined_raw.parquet'
    synthetic = A/'BF16_reverse_rank_CDF_synthetic_preflight_v1_20261008/verification.json'
    assert read(synthetic)['status'] == 'passed_actual39_reverse_BF16_synthetic_CDF_and78_day_controls'
    paths = [Path(__file__), Path(codec.__file__), plan_path, frame_path, parent_path, neural_path,
             neural_folder/'verification.json', synthetic,
             *[A/f'optimization_20261003_r{n}'/name for n in parents for name in ('selection.json','protocol.json','calibrated_csv_official.json','full_registration_execution.json')]]
    pins = {**neural_proof['input_sha256'], **{str(p):sha(p) for p in paths}}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual_full37_controls.json', {'input_sha256':pins,'plan':plan,
        'actual_full_qualified_parent_round':parent,'baseline_metrics':metrics,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    while psutil.virtual_memory().available < 9*2**30:time.sleep(15)
    keys = ['ts_code','trade_date']
    frame = pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid'])
    neural_frame = pl.read_parquet(neural_path)
    assert neural_frame.select(keys).equals(frame.select(keys))
    dates = frame['trade_date'].to_numpy();flags = frame['flag_limit_up'].to_numpy();valid = frame['price_valid'].to_numpy()
    assert len(frame)==5635800 and frame['trade_date'].n_unique()==1212 and frame['ts_code'].n_unique()==4650
    raw = np.load(parent_path,mmap_mode='r');neural = neural_frame['pred_raw'].to_numpy()
    assert raw.dtype==neural.dtype==np.float64
    prepared = codec.prepare(raw,neural,dates,flags,valid)
    cases = [(role,weight) for role in plan['roles'] for weight in plan['weights']]+[('all_valid',0.)]
    assert len(cases)==37
    records = []
    for case,(role,weight) in enumerate(cases):
        started = time.monotonic()
        actual = codec.apply_prepared(raw,flags,valid,role,weight,prepared)
        oracle = codec.pandas_oracle(raw,neural,dates,flags,valid,role,weight)
        assert np.array_equal(actual.view('u8'),oracle.view('u8'))
        selected = codec.selected(flags,valid,role)
        assert np.array_equal(actual[~selected].view('u8'),np.asarray(raw)[~selected].view('u8'))
        cold = []
        for days in (80,260,975):
            n = days*4650
            prefix = codec.transform(raw[:n],neural[:n],dates[:n],flags[:n],valid[:n],role,weight)
            independent = codec.pandas_oracle(raw[:n],neural[:n],dates[:n],flags[:n],valid[:n],role,weight)
            assert np.array_equal(prefix.view('u8'),actual[:n].view('u8'))
            assert np.array_equal(independent.view('u8'),actual[:n].view('u8'))
            cold.append({'days':days,'rows':n,'native_and_Pandas_prefix_bits_exact':True})
        record = {'case':case,'role':role,'weight':weight,'rows':len(actual),'controls':cold,
                  'full_independent_Pandas_CDF_bits_exact':True,'declared_unselected_forecast_bits_preserved':True,
                  'first2020_changed_rows':int(np.count_nonzero(actual[dates<20210101]!=raw[dates<20210101])),
                  'elapsed_seconds':time.monotonic()-started}
        if weight==0.:assert np.array_equal(actual.view('u8'),np.asarray(raw).view('u8'))
        create(OUT/f'case{case:02d}.json',record);records.append(record)
        del actual,oracle,prefix,independent;gc.collect()
        print(f'Actual full BF16 rank-CDF {case+1}/37: {role},weight={weight:g}; three cold prefixes exact',flush=True)
    for p,d in pins.items():assert sha(p)==d,p
    create(OUT/'verification.json', {'status':'passed_actual37_full5635800_reverse_BF16_CDF_independent_and111_cold_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_parent_round':parent,
        'controls':records,'rows_days_stocks':[5635800,1212,4650], 'actual_full_cases':37,'actual_cold_cases':111,
        'first2020_not_assumed_identity':True,'all_original_parent_native_and_extra_branches_preserved_before_new_stage':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_BF16_reverse_rank_CDF_full37_location_v1_20261008.json', {
        'status':'actual_full37_BF16_rank_CDF_controls_passed_on_E','output':str(OUT),
        'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})


if __name__ == '__main__':main()

