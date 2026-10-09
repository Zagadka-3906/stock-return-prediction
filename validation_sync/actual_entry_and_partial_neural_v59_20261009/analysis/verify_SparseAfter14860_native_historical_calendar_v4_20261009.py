"""Replay the frozen Huber/sparse mixture using own historical models and the final2025 model on remapped training dates."""
from pathlib import Path
from types import SimpleNamespace
import os
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
for option in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[option]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/SparseAfter14860_native_historical_calendar_v1_20261009')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'service_execution.json').exists():time.sleep(10)
    while owned(read(folder/'native_launch.json')):time.sleep(1)
    assert read(folder/'service_execution.json')['status']=='passed',name


def main():
    closed('AdaptiveJointCrossHuber242_round148_full_registration_v8_20261009')
    import numpy as np
    import polars as pl
    import psutil
    from run import FEATURE_FILE,feature_names
    import SparseAfter148_complete_parent_CDF_v1_20261009 as codec
    from SparseAfter148_complete_parent_native_stage_v1_20261009 import after_parent,GRAPH_KEY,exact
    proposal=A/'SparseAfter14829_round152_proposal_v1_20261009.json';plan=read(proposal)
    synthetic=A/'SparseAfter14829_synthetic25_and_state10_metadata_v1_20261009.json';proof=read(synthetic)
    assert proof['actual_cases']==25 and proof['actual_cold_cases']==75 and len(proof['actual_existing_state_metadata'])==10
    assert not proof['new_native_fits'] and len(plan['heads'])==2
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet'
    teacherpath=A/'optimization_20261003_r106/selected_validation.npy'
    parentpath=A/'optimization_20261003_r148/selected_validation.npy'
    sources=[Path(__file__),proposal,synthetic,Path(codec.__file__),A/'SparseAfter148_complete_parent_native_stage_v1_20261009.py',
        A/'HuberCrossFamily_complete_parent_CDF_v1_20261008.py',A/'nonflag_sparse_Gram64_codec_20261007.py',
        A/'nonflag_residual_Ridge_codec_20261007.py',A/'nonflag_HuberIRLS64_streamed_v1_20261008.py',
        FEATURE_FILE,framepath,teacherpath,parentpath]
    pins={**proof['input_sha256'],**{str(path):sha(path) for path in sources}}
    OUT.mkdir(exist_ok=False)
    cases=[{'group':g,'share':.5,'amplitude':a} for g in range(6) for a in (.0005,.00325)]
    assert len(cases)==12
    create(OUT/'frozen_before_actual60_native_controls.json',{
        'input_sha256':pins,'historical_years':[2021,2022,2023,2024],
        'final_model_year':2025,'remapped_training_date_calendar_years':[2025,2026],
        'actual_control_cases':cases,'expected_historical_cases':48,'expected_calendar_cases':12,
        'expected_cold_cases':60,'expected_prefit_date_rejections':12,
        'actual_future_X_and_labels_read':False,'new_native_fits':0,'new_quality_scores':0})
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    names=feature_names();keys=['ts_code','trade_date']
    frame=pl.read_parquet(framepath,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy()
    assert (len(frame),frame['trade_date'].n_unique(),frame['ts_code'].n_unique())==(5635800,1212,4650)
    assert dates.max()<20250101
    teacher=np.load(teacherpath,mmap_mode='r');parent=np.load(parentpath,mmap_mode='r')
    saved={h:np.load(row['oof'],mmap_mode='r') for h,row in plan['heads'].items()}
    def components(case,year):
        required=list(dict.fromkeys(h for group,sign in codec.GROUPS[case['group']] for h in group))
        result=[]
        for head in required:
            row=plan['heads'][head];info=read(row['infos'][str(year)])
            assert row['state_kind']=='linear'
            result.append({'head':head,'name':info['name'],'state_kind':row['native_stage_state_kind'],
                'path':info['native_model_path'],'sha256':info['native_model_sha256'],
                'independent_state_path':info['independent_linear_state_path'],
                'independent_state_sha256':info['independent_linear_state_sha256'],'training_info':info})
        return result
    def specification(case):
        return {**case,'original_complete_parent_round':148,'universe':'all_current_raw_forecasts',
            'position':'after_complete_qualified_parent','teacher_feature':'qualified106_current_forecast_average_rank_over_N'}
    records=[]
    for year in (2021,2022,2023,2024,2025):
        historical=year<2025;training_year=year if historical else 2024
        days=np.unique(dates[dates//10000==training_year])[:3 if historical else 2]
        positions=np.flatnonzero(np.isin(dates,days));panel=frame[positions]
        test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
        assert test.select(keys).equals(panel.select(keys)) and not {'y_rank','y_ret_1d'}&set(test.columns)
        actual_dates=panel['trade_date'].to_numpy() if historical else np.repeat(np.array([20250102,20260102]),4650)
        features=test.select(names).to_numpy().astype(np.float64)
        current_teacher=np.asarray(teacher[positions],dtype=np.float64)
        base=np.asarray(parent[positions],dtype=np.float64)
        raw={h:x[positions] for h,x in saved.items()} if historical else None
        for case in cases:
            spec=specification(case)
            context=SimpleNamespace(dates=actual_dates,flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                _nonflag_raw_features=features,_nonflag_raw_feature_names=names,_whole_graph={GRAPH_KEY:spec})
            value,report=after_parent(SimpleNamespace(read=read,sha=sha),context,current_teacher,base,spec,components(case,year))
            if historical:
                residual=codec.mixture(raw,case['group'],case['share'])
                exact(value,codec.transform(base,residual,context.dates,context.flags,context.valid,case['amplitude']))
                exact(value,codec.pandas_oracle(base,codec.independent_mixture(raw,case['group'],case['share']),context.dates,context.flags,context.valid,case['amplitude']))
            cold=SimpleNamespace(**vars(context))
            for name in ('dates','flags','valid','_nonflag_raw_features'):setattr(cold,name,getattr(context,name)[:4650])
            prefix,cold_report=after_parent(SimpleNamespace(read=read,sha=sha),cold,current_teacher[:4650],base[:4650],spec,components(case,year))
            exact(prefix,value[:4650])
            if not historical:
                bad=SimpleNamespace(**vars(cold));bad.dates=np.full(4650,20240102);rejected=False
                try:after_parent(SimpleNamespace(read=read,sha=sha),bad,current_teacher[:4650],base[:4650],spec,components(case,year))
                except AssertionError:rejected=True
                assert rejected
            row={'mode':'own_historical_model' if historical else 'final2025_model_on_remapped_training_dates',
                'year':year,'configuration':case,'full':report,'cold':cold_report,
                'saved_OOF_bits_exact':historical,'prefit2024_dates_rejected':not historical,
                'actual_future_features_not_read':True}
            create(OUT/f'control{len(records):03d}.json',row);records.append(row)
            print({'controls':len(records),'expected':60,'year':year},flush=True)
    assert len(records)==60
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual48_SparseAfter148_all5_annual_native_and12_final_calendar_with60_cold_and12_prefit_rejections',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
        'actual_historical_cases':48,'actual_calendar_cases':12,'actual_cold_cases':60,
        'actual_prefit_final_model_date_rejections':12,'actual_existing_annual_states':10,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_and_labels_read':False})
    create(A/'actual_SparseAfter14860_native_calendar_location_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})


if __name__=='__main__':main()
