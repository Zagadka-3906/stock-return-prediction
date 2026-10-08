"""Fifteen actual historical native ensemble hooks; never reads future features or labels."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/ConeRidgeAlpha48_native_historical_hooks_v1_20261008')


def main():
    folder=A/'service_owned_workflows_20261006/ConeRidgeAlpha97_parent134_historical_controls_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names
    from ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008 import GROUPS,mixture,transform
    from ConeRidgeAlpha8_64_complete_parent_native_stage_v1_20261008 import after_parent,GRAPH_KEY,exact
    plan_path=A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json';plan=read(plan_path)
    frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    teacher_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r134/selected_validation.npy'
    proof=Path(read(A/'actual_ConeRidgeAlpha97_parent134_location_v1_20261008.json')['output'])/'verification.json'
    assert read(proof)['actual_full_cases']==97 and read(proof)['actual_cold_cases']==291
    sources=[Path(__file__),A/'ConeRidgeAlpha8_64_complete_parent_native_stage_v1_20261008.py',A/'ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008.py',
             plan_path,frame_path,FEATURE_FILE,teacher_path,parent_path,proof]
    for head,row in plan['heads'].items():
        sources.append(Path(row['oof']))
        for year in (2021,2022,2024):
            path=Path(row['infos'][str(year)]);info=read(path);sources += [path,Path(info['native_model_path']),Path(info['independent_'+row['state_kind']+'_state_path'])]
    pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    assert not OUT.exists();OUT.mkdir(parents=True)
    create(OUT/'frozen_before_actual48_historical_hooks.json',{'input_sha256':pins,'historical_years':[2021,2022,2024],'groups':16,'new_quality_scores':0,'actual_future_X_and_labels_read':False})
    names=feature_names();keys=['ts_code','trade_date']
    frame=pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy()
    all_teacher=np.load(teacher_path,mmap_mode='r');all_parent=np.load(parent_path,mmap_mode='r')
    arrays={head:np.load(row['oof'],mmap_mode='r') for head,row in plan['heads'].items()};records=[]
    for year,share,amplitude in zip((2021,2022,2024),(.5,.5,.5),(.005,.025,.1)):
        days=np.unique(dates[dates//10000==year])[:3];positions=np.flatnonzero(np.isin(dates,days));panel=frame[positions]
        test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
        assert test.select(keys).equals(panel.select(keys)) and len(panel)==3*4650 and not {'y_rank','y_ret_1d'}&set(test.columns)
        teacher=np.asarray(all_teacher[positions],dtype=np.float64);parent=np.asarray(all_parent[positions],dtype=np.float64)
        for group in range(16):
            spec={'group':group,'share':share,'amplitude':amplitude,'universe':'all_current_raw_forecasts','position':'after_complete_qualified_parent',
                  'teacher_feature':'qualified106_current_forecast_average_rank_over_N'}
            components=[]
            for head in dict.fromkeys(h for members,sign in GROUPS[group] for h in members):
                row=plan['heads'][head];info=read(row['infos'][str(year)]);kind=row['state_kind']
                components.append({'head':head,'name':info['name'],'state_kind':row['native_stage_state_kind'],'path':info['native_model_path'],'sha256':info['native_model_sha256'],
                    'independent_state_path':info['independent_'+kind+'_state_path'],'independent_state_sha256':info['independent_'+kind+'_state_sha256'],'training_info':info})
            context=SimpleNamespace(dates=panel['trade_date'].to_numpy(),flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                _nonflag_raw_features=test.select(names).to_numpy().astype(np.float64),_nonflag_raw_feature_names=names,_whole_graph={GRAPH_KEY:spec})
            value,full=after_parent(SimpleNamespace(sha=sha,read=read),context,teacher,parent,spec,components)
            residual=mixture({h:array[positions] for h,array in arrays.items()},group,share)
            exact(value,transform(parent,residual,context.dates,context.flags,context.valid,amplitude))
            cold_context=SimpleNamespace(**vars(context))
            for field in ('dates','flags','valid','_nonflag_raw_features'):setattr(cold_context,field,getattr(context,field)[:4650])
            prefix,cold=after_parent(SimpleNamespace(sha=sha,read=read),cold_context,teacher[:4650],parent[:4650],spec,components);exact(prefix,value[:4650])
            record={'year':year,'group':group,'share':share,'amplitude':amplitude,'full':full,'cold':cold,'saved_OOF_mixture_and_native_stage_bits_exact':True,'whole_day_prefix_bits_exact':True}
            create(OUT/f'hook{len(records)+1}.json',record);records.append(record)
            print(f'Actual cross-family native historical hook {len(records)}/48: {year} group{group}',flush=True)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual48_ConeRidge_native_historical_hooks_and48_cold_prefixes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_hooks':48,'actual_cold_hooks':48,
        'new_quality_scores':0,'new_native_fits':0,'actual_future_X_and_labels_read':False,'final144_parent_controls_and_source_admission_still_required':True})
    create(A/'actual_ConeRidgeAlpha48_native_hooks_location_v1_20261008.json',{'status':'passed_actual48_ConeRidge_native_historical_hooks_on_E','output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
